from decimal import Decimal
from django.test import TestCase
from .models import Product, Box, Order, OrderItem
from .services import recommend_box_for_order, NoSuitableBoxError


class BoxRecommendationTests(TestCase):
    def setUp(self):
        # Boxes, smallest to largest, cheapest to costliest
        self.small_box = Box.objects.create(
            name="Small", internal_length_cm=20, internal_width_cm=15,
            internal_height_cm=10, max_weight_kg=5, cost=30,
        )
        self.medium_box = Box.objects.create(
            name="Medium", internal_length_cm=35, internal_width_cm=25,
            internal_height_cm=20, max_weight_kg=10, cost=50,
        )
        self.large_box = Box.objects.create(
            name="Large", internal_length_cm=50, internal_width_cm=40,
            internal_height_cm=30, max_weight_kg=20, cost=80,
        )

        self.phone_case = Product.objects.create(
            name="Phone Case", length_cm=15, width_cm=8, height_cm=2, weight_kg=Decimal("0.1"),
        )
        self.book = Product.objects.create(
            name="Book", length_cm=22, width_cm=15, height_cm=3, weight_kg=Decimal("0.4"),
        )
        self.giant_sofa = Product.objects.create(
            name="Giant Sofa", length_cm=200, width_cm=100, height_cm=100, weight_kg=50,
        )

    def test_recommends_cheapest_box_that_fits(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.phone_case, quantity=2)
        OrderItem.objects.create(order=order, product=self.book, quantity=1)

        result = recommend_box_for_order(order)

        # Book's longest side (22cm) exceeds the small box's longest
        # internal side (20cm), so it correctly needs the medium box.
        self.assertEqual(result.box, self.medium_box)

    def test_heavier_order_needs_bigger_box(self):
        order = Order.objects.create()
        # Enough books to exceed the small box's weight limit but not medium's
        OrderItem.objects.create(order=order, product=self.book, quantity=15)

        result = recommend_box_for_order(order)

        self.assertEqual(result.box, self.medium_box)

    def test_no_box_fits_raises_error(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.giant_sofa, quantity=1)

        with self.assertRaises(NoSuitableBoxError):
            recommend_box_for_order(order)

    def test_empty_order_raises_error(self):
        order = Order.objects.create()

        with self.assertRaises(NoSuitableBoxError):
            recommend_box_for_order(order)