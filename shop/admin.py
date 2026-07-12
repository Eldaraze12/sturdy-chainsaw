from django.contrib import admin
from django.utils.html import format_html

from .models import Category, ContactMessage, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "product_count")
    list_editable = ("order",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Məhsul sayı")
    def product_count(self, obj):
        return obj.products.count()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "phone", "subject", "message")
    actions = ("mark_as_read",)

    @admin.action(description="Oxunmuş kimi işarələyin")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "category",
        "price",
        "stock",
        "is_available",
        "is_featured",
    )
    list_editable = ("price", "stock", "is_available", "is_featured")
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25
    autocomplete_fields = ("category",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")

    @admin.display(description="Şəkil")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;'
                'border-radius:8px;" />',
                obj.image.url,
            )
        return "—"


admin.site.site_header = "Şirin Anlar İdarəetmə"
admin.site.site_title = "Şirin Anlar"
admin.site.index_title = "İdarəetmə paneli"
