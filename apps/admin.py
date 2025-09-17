from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "image")
    search_fields = ("title", "description")
    list_filter = ("title",)
    ordering = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "created_at")
    search_fields = ("title", "description")
    list_filter = ("category", "price")
    ordering = ("-created_at",)
