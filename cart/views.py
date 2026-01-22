from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from shop.models import Product


class CartDetailView(generics.RetrieveAPIView):
    """Получение корзины пользователя"""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemCreateView(generics.CreateAPIView):
    """Добавление товара в корзину"""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])

        # Проверяем, есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": serializer.validated_data.get("quantity", 1)},
        )

        if not created:
            cart_item.quantity += serializer.validated_data.get("quantity", 1)
            cart_item.save()


class CartItemUpdateView(generics.UpdateAPIView):
    """Обновление количества товара в корзине"""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = CartItem.objects.all()

    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs["pk"])


class CartItemDeleteView(generics.DestroyAPIView):
    """Удаление товара из корзины"""

    permission_classes = [permissions.IsAuthenticated]

    queryset = CartItem.objects.all()

    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs["pk"])


class CartClearView(APIView):
    """Очистка корзины"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({"message": "Корзина очищена"}, status=status.HTTP_200_OK)
