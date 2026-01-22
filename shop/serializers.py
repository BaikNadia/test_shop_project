from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории"""

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "parent", "subcategories"]

    def get_subcategories(self, obj):
        """Получить подкатегории"""
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True).data
        return []


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений товара"""

    class Meta:
        model = ProductImage
        fields = ["original", "medium", "small"]


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара"""

    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    parent_category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_name",
            "parent_category",
            "price",
            "images",
        ]

    def get_parent_category(self, obj):
        """Получить родительскую категорию"""
        if obj.category.parent:
            return {
                "id": obj.category.parent.id,
                "name": obj.category.parent.name,
                "slug": obj.category.parent.slug,
            }
        return None
