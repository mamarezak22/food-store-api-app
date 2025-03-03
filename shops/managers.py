from django.db.models import Manager

class OpenStoreManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_store_open = True)
