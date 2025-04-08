from rest_framework import serializers

class ProductValidator(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            "required": "Product name is required.",
            "max_length": "Name must not exceed 100 characters."
        }
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            "required": "Price is required.",
            "invalid": "Enter a valid price amount."
        }
    )
    color = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            "required": "Color is required.",
            "max_length": "Color must not exceed 50 characters."
        }
    )
    offer = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        error_messages={
            "max_length": "Offer must not exceed 100 characters."
        }
    )
