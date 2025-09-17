from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Category, Product


class CategorySerializer(ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ("id", "title", "description", "image")


class ProductSerializer(ModelSerializer):
    """Serializer for Product model."""

    category = CategorySerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "image",
            "description",
            "category",
            "category_id",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
