from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version="v1",
        description="API для интернет-магазина",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@shop.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Главная страница
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    # Admin
    path("admin/", admin.site.urls),
    # API
    path(
        "api/",
        include(
            [
                # Authentication
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
                ),
                # Shop (теперь все в shop.urls)
                path("", include("shop.urls")),
            ]
        ),
    ),
    # Cart
    path("api/cart/", include("cart.urls")),
    # Documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
