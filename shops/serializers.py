from rest_framework import serializers
from .models import Store, Food

class StoreListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

class FoodListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name','description','image','category','final_price','discount_rate','counts']






