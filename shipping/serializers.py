from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            "id", "name",
            "internal_length_cm", "internal_width_cm", "internal_height_cm",
            "max_weight_kg", "cost",
        ]


class BoxRecommendationSerializer(serializers.Serializer):
    box = BoxSerializer()
    reason = serializers.CharField()