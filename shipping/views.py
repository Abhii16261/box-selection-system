from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .services import recommend_box_for_order, NoSuitableBoxError
from .serializers import BoxRecommendationSerializer


@api_view(["GET"])
def recommend_box_view(request, order_id):
    """
    GET /api/orders/<order_id>/recommend-box/

    Returns the cheapest Box that fits the given order, or a 404-style
    error response if no box fits.
    """
    order = get_object_or_404(Order, id=order_id)

    try:
        result = recommend_box_for_order(order)
    except NoSuitableBoxError as e:
        return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    serializer = BoxRecommendationSerializer(result)
    return Response(serializer.data)