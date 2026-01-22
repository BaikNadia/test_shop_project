from rest_framework import serializers
from .models import Cart, CartItem
from shop.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента корзины"""

    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "total_price", "added_at"]


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины"""

    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "total_items",
            "total_price",
            "created_at",
            "updated_at",
        ]
