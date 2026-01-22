from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart-detail"),
    path("items/", views.CartItemCreateView.as_view(), name="cart-item-create"),
    path(
        "items/<int:pk>/", views.CartItemUpdateView.as_view(), name="cart-item-update"
    ),
    path(
        "items/<int:pk>/delete/",
        views.CartItemDeleteView.as_view(),
        name="cart-item-delete",
    ),
    path("clear/", views.CartClearView.as_view(), name="cart-clear"),
]
