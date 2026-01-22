from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(
            name="Тестовая родительская категория", slug="test-parent-category"
        )
        self.child_category = Category.objects.create(
            name="Тестовая дочерняя категория",
            slug="test-child-category",
            parent=self.parent_category,
        )
        self.url = reverse("category-list")

    def test_get_categories_success(self):
        """Тест успешного GET запроса для категорий"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["name"], "Тестовая родительская категория"
        )

    def test_category_has_subcategories(self):
        """Тест наличия подкатегорий в ответе"""
        response = self.client.get(self.url)

        self.assertEqual(len(response.data["results"][0]["subcategories"]), 1)
        self.assertEqual(
            response.data["results"][0]["subcategories"][0]["name"],
            "Тестовая дочерняя категория",
        )


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Тестовая категория", slug="test-category"
        )
        self.product = Product.objects.create(
            name="Тестовый товар",
            slug="test-product",
            category=self.category,
            price=1000.00,
        )
        self.url = reverse("product-list")

    def test_get_products_success(self):
        """Тест успешного GET запроса для товаров"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Тестовый товар")
        self.assertEqual(float(response.data["results"][0]["price"]), 1000.00)

    def test_product_has_category_info(self):
        """Тест наличия информации о категории у товара"""
        response = self.client.get(self.url)

        product_data = response.data["results"][0]
        self.assertEqual(product_data["category_name"], "Тестовая категория")
        self.assertIsNotNone(product_data["category"])
