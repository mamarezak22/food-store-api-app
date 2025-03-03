from rest_framework import serializers
from .models import Store

class StoreListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"








