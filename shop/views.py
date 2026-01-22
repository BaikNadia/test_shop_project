from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(generics.ListAPIView):
    """Список категорий с подкатегориями"""

    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Только категории без родителя
        return Category.objects.filter(parent=None)


class ProductListView(generics.ListAPIView):
    """Список товаров"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "category__parent"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
