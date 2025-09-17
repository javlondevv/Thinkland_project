from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from elasticsearch import Elasticsearch, NotFoundError

from apps.models import Product

es = Elasticsearch(settings.ELASTICSEARCH_HOST)
INDEX = "products"


@receiver(post_save, sender=Product)
def index_product(sender, instance: Product, **kwargs):
    """
    Index or update a product in Elasticsearch whenever it is saved.
    """
    if not es.ping():
        return

    doc = {
        "id": instance.id,
        "title": instance.title,
        "description": instance.description,
        "price": float(instance.price),
        "category_id": instance.category_id,
        "category_title": instance.category.title if instance.category else "",
        "created_at": instance.created_at.isoformat() if instance.created_at else None,
    }

    try:
        es.index(index=INDEX, id=instance.id, body=doc, refresh=True)
    except Exception as exc:
        print(f"❌ Failed to index product {instance.id}: {exc}")


@receiver(post_delete, sender=Product)
def delete_product(sender, instance: Product, **kwargs):
    """
    Remove a product from Elasticsearch whenever it is deleted.
    """
    if not es.ping():
        return

    try:
        es.delete(index=INDEX, id=instance.id, refresh=True)
    except NotFoundError:
        pass
    except Exception as exc:
        print(f"❌ Failed to delete product {instance.id} from Elasticsearch: {exc}")
