"""
Core box-selection logic.

Given an order (a collection of products + quantities), determine which
Box is the cheapest one that can physically hold the order.

Approach (documented simplification — see README):
- We do NOT perform true 3D bin-packing (deciding exact x/y/z placement of
  every item), because that is a computationally hard problem out of scope
  for this assignment.
- Instead, a box is considered "suitable" if:
    1. Total weight of all items <= box.max_weight_kg
    2. Total volume of all items <= box.volume_cm3
    3. Every individual item's longest dimension fits within the box's
       longest internal dimension (a basic sanity check so we don't, say,
       recommend a small flat box for one giant single item just because
       the box has enough total volume).
- Among all suitable boxes, we recommend the cheapest one.
"""

from dataclasses import dataclass
from decimal import Decimal

from .models import Box, Order


@dataclass
class BoxRecommendation:
    box: Box
    reason: str


class NoSuitableBoxError(Exception):
    """Raised when no box in the system can fit the given order."""
    pass


def _order_totals(order: Order):
    """Compute total weight and total volume for all items in an order."""
    total_weight = Decimal("0")
    total_volume = Decimal("0")
    item_dimensions = []  # list of (length, width, height) per unit, repeated by qty

    for order_item in order.orderitem_set.select_related("product"):
        product = order_item.product
        qty = order_item.quantity
        total_weight += product.weight_kg * qty
        total_volume += product.volume_cm3 * qty
        for _ in range(qty):
            item_dimensions.append(
                (product.length_cm, product.width_cm, product.height_cm)
            )

    return total_weight, total_volume, item_dimensions


def _fits_by_longest_dimension(item_dims, box: Box) -> bool:
    """
    Sanity check: every item's longest side must fit within the box's
    longest internal side. This catches obviously-impossible cases that a
    pure volume/weight check would miss (e.g. one long thin item vs a
    small cube-shaped box with the same volume).
    """
    box_longest = max(box.internal_length_cm, box.internal_width_cm, box.internal_height_cm)
    for length, width, height in item_dims:
        item_longest = max(length, width, height)
        if item_longest > box_longest:
            return False
    return True


def recommend_box_for_order(order: Order) -> BoxRecommendation:
    """
    Return the cheapest Box that can hold the given order.
    Raises NoSuitableBoxError if no box qualifies.
    """
    total_weight, total_volume, item_dims = _order_totals(order)

    if not item_dims:
        raise NoSuitableBoxError("Order has no items; cannot recommend a box.")

    candidate_boxes = Box.objects.all().order_by("cost")

    for box in candidate_boxes:
        if total_weight > box.max_weight_kg:
            continue
        if total_volume > box.volume_cm3:
            continue
        if not _fits_by_longest_dimension(item_dims, box):
            continue

        return BoxRecommendation(
            box=box,
            reason=(
                f"Order weight {total_weight}kg <= box max {box.max_weight_kg}kg; "
                f"order volume {total_volume}cm3 <= box volume {box.volume_cm3}cm3; "
                f"cheapest suitable box."
            ),
        )

    raise NoSuitableBoxError(
        f"No box can fit this order (total weight={total_weight}kg, "
        f"total volume={total_volume}cm3)."
    )