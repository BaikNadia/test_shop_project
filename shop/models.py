from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категория товаров"""

    name = models.CharField(max_length=200, verbose_name="Наименование")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to="categories/", verbose_name="Изображение")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Родительская категория",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def is_parent(self):
        return self.parent is None


class Product(models.Model):
    """Товар"""

    name = models.CharField(max_length=200, verbose_name="Наименование")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def parent_category(self):
        """Возвращает родительскую категорию, если подкатегория"""
        if self.category.parent:
            return self.category.parent
        return self.category


class ProductImage(models.Model):
    """Изображение товара"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Товар"
    )
    original = models.ImageField(
        upload_to="products/original/", verbose_name="Оригинал"
    )
    medium = models.ImageField(
        upload_to="products/medium/", verbose_name="Среднее", blank=True
    )
    small = models.ImageField(
        upload_to="products/small/", verbose_name="Маленькое", blank=True
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Изображение {self.product.name}"
