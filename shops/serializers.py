from rest_framework import serializers
from .models import Store, Food,StoreWorkingHour,Category,FoodComment,City

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreWorkingHour
        fields = "__all__"

class CategorySeriliazer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class CitySeriliazer(serializers.ModelSerializer):
    class Meta:
        model =


class StoreListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

class FoodListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name','description','image','category','final_price','discount_rate','counts']






