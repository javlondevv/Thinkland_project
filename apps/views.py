from django.conf import settings
from elasticsearch import Elasticsearch
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

es = Elasticsearch(settings.ELASTICSEARCH_HOST)


class CategoryViewSet(ModelViewSet):
    """ViewSet for managing product categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProductViewSet(ModelViewSet):
    """ViewSet for managing products with Elasticsearch search integration."""

    queryset = Product.objects.select_related("category").all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_description="Search products by title, description, or category using Elasticsearch",
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True,
                example="iPhone"
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of products matching the search query",
                schema=ProductSerializer(many=True)
            ),
            400: openapi.Response(
                description="Bad Request - Query parameter 'q' is required",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Query parameter 'q' is required."
                        )
                    }
                )
            ),
            500: openapi.Response(
                description="Internal Server Error - Elasticsearch connection issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Connection error"
                        )
                    }
                )
            )
        }
    )
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """Search products by title, description, or category using Elasticsearch."""
        query = request.query_params.get("q")
        if not query:
            return Response(
                {"detail": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "description", "category_title"],
                }
            }
        }

        try:
            response = es.search(index="products", body=body)
            product_ids = [hit["_source"]["id"] for hit in response.get("hits", {}).get("hits", [])]
            products = Product.objects.filter(id__in=product_ids).select_related("category")
        except Exception as exc:
            # Fallback to database search if Elasticsearch is not available
            products = Product.objects.filter(
                title__icontains=query
            ).select_related("category")
            if not products.exists():
                products = Product.objects.filter(
                    description__icontains=query
                ).select_related("category")
            if not products.exists():
                products = Product.objects.filter(
                    category__title__icontains=query
                ).select_related("category")

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
