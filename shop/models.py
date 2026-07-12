from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Ad", max_length=100, unique=True)
    slug = models.SlugField("Slug (ünvan)", max_length=120, unique=True, blank=True)
    description = models.TextField("Təsvir", blank=True)
    order = models.PositiveIntegerField("Sıra", default=0)

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)

    def featured(self):
        return self.filter(is_featured=True)

    def in_category(self, category):
        return self.filter(category=category)

    def search(self, query):
        return self.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Kateqoriya",
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField("Ad", max_length=150)
    slug = models.SlugField("Slug (ünvan)", max_length=170, unique=True, blank=True)
    description = models.TextField("Təsvir", blank=True)
    price = models.DecimalField("Qiymət (₼)", max_digits=8, decimal_places=2)
    image = models.ImageField("Şəkil", upload_to="products/", blank=True, null=True)

    stock = models.PositiveIntegerField("Stok (ədəd)", default=0)
    is_available = models.BooleanField("Satışdadır", default=True)

    is_featured = models.BooleanField("Ana səhifədə göstər", default=False)
    created_at = models.DateTimeField("Yaradılma tarixi", auto_now_add=True)
    updated_at = models.DateTimeField("Yenilənmə tarixi", auto_now=True)

    objects: ProductQuerySet = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_available", "is_featured"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    @property
    def in_stock(self):
        return self.is_available and self.stock > 0


class ContactMessage(models.Model):
    name = models.CharField("Ad", max_length=100)
    phone = models.CharField("Telefon", max_length=30)
    subject = models.CharField("Mövzu", max_length=150)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField("Göndərilmə tarixi", auto_now_add=True)
    is_read = models.BooleanField("Oxunub", default=False)

    class Meta:
        verbose_name = "Əlaqə mesajı"
        verbose_name_plural = "Əlaqə mesajları"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject}"
