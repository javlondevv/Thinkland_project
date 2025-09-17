from django.db.models import Model, CharField, TextField, ImageField, DateTimeField, ForeignKey, DecimalField, CASCADE


class Category(Model):
    """Represents a product category."""

    title = CharField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="Name of the category"
    )
    description = TextField(
        blank=True,
        help_text="Optional category description"
    )
    image = ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Category image"
    )
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title or "Unnamed Category"


class Product(Model):
    """Represents a product belonging to a category."""

    category = ForeignKey(
        Category,
        related_name="products",
        on_delete=CASCADE
    )
    title = CharField(
        max_length=255,
        db_index=True,
        help_text="Product title"
    )
    price = DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Product price"
    )
    image = ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Product image"
    )
    description = TextField(
        blank=True,
        help_text="Optional product description"
    )
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title
