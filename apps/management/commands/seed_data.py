from django.core.management.base import BaseCommand
from django.db import transaction
from apps.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with realistic categories and products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Successfully cleared existing data"))

        with transaction.atomic():
            # Create categories
            categories_data = [
                {
                    "title": "Electronics & Gadgets",
                    "description": "Cutting-edge technology and electronic devices for modern living. From smartphones to smart home devices, find the latest innovations to enhance your digital lifestyle.",
                },
                {
                    "title": "Home & Garden",
                    "description": "Everything you need to create a beautiful and comfortable living space. From furniture and decor to gardening tools and outdoor equipment.",
                },
                {
                    "title": "Sports & Fitness",
                    "description": "Gear up for an active lifestyle with our comprehensive collection of sports equipment, fitness accessories, and athletic wear for all skill levels.",
                },
            ]

            categories = []
            for cat_data in categories_data:
                category, created = Category.objects.get_or_create(
                    title=cat_data["title"], defaults=cat_data
                )
                categories.append(category)
                if created:
                    self.stdout.write(f"Created category: {category.title}")

            # Create products
            products_data = [
                # Electronics & Gadgets
                {
                    "category": categories[0],
                    "title": "iPhone 15 Pro Max",
                    "price": 1199.99,
                    "description": "The most advanced iPhone ever with titanium design, A17 Pro chip, and professional camera system. Features 6.7-inch Super Retina XDR display and all-day battery life.",
                },
                {
                    "category": categories[0],
                    "title": "Samsung Galaxy S24 Ultra",
                    "price": 1299.99,
                    "description": "Premium Android smartphone with S Pen, 200MP camera, and AI-powered features. Built with titanium frame and Gorilla Glass Victus 2 for ultimate durability.",
                },
                {
                    "category": categories[0],
                    "title": "MacBook Air M3",
                    "price": 1099.99,
                    "description": "Ultra-thin laptop with Apple M3 chip delivering incredible performance and battery life. Perfect for productivity, creativity, and everyday computing tasks.",
                },
                {
                    "category": categories[0],
                    "title": "Sony WH-1000XM5 Headphones",
                    "price": 399.99,
                    "description": "Industry-leading noise canceling wireless headphones with 30-hour battery life, crystal clear hands-free calling, and quick charge technology.",
                },
                # Home & Garden
                {
                    "category": categories[1],
                    "title": "Dyson V15 Detect Cordless Vacuum",
                    "price": 749.99,
                    "description": "Advanced cordless vacuum with laser dust detection, powerful suction, and intelligent cleaning modes. Automatically adjusts suction power based on floor type.",
                },
                {
                    "category": categories[1],
                    "title": "KitchenAid Stand Mixer",
                    "price": 429.99,
                    "description": "Professional-grade stand mixer with 5-quart stainless steel bowl, 10 speeds, and multiple attachments. Perfect for baking enthusiasts and home chefs.",
                },
                {
                    "category": categories[1],
                    "title": "Casper Original Mattress",
                    "price": 1095.00,
                    "description": "Award-winning memory foam mattress designed for optimal comfort and support. Features breathable foam layers and temperature regulation for better sleep.",
                },
                {
                    "category": categories[1],
                    "title": "Philips Hue Smart Bulb Starter Kit",
                    "price": 199.99,
                    "description": "Smart lighting system with color-changing LED bulbs, wireless dimmer switch, and smartphone app control. Compatible with Alexa and Google Assistant.",
                },
                # Sports & Fitness
                {
                    "category": categories[2],
                    "title": "Peloton Bike+",
                    "price": 2495.00,
                    "description": "Premium indoor cycling bike with 24-inch rotating touchscreen, auto-follow resistance, and access to thousands of live and on-demand classes.",
                },
                {
                    "category": categories[2],
                    "title": "Nike Air Zoom Pegasus 40",
                    "price": 130.00,
                    "description": "Versatile running shoe with responsive Zoom Air cushioning, breathable mesh upper, and durable rubber outsole. Perfect for daily training and long-distance running.",
                },
            ]

            for product_data in products_data:
                product, created = Product.objects.get_or_create(
                    title=product_data["title"], defaults=product_data
                )
                if created:
                    self.stdout.write(f"Created product: {product.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database with {len(categories)} categories and {len(products_data)} products!"
            )
        )
