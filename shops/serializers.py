from rest_framework import serializers
from .models import Store, Food,StoreWorkingHour,Category,FoodComment,City

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreWorkingHour
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class StoreListViewSerializer(serializers.ModelSerializer):
    working_hour = WorkingHourSerializer()
    city = CitySerializer()
    class Meta:
        model = Store
        fields = "__all__"

class FoodListViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Food
        fields = ['name','description','image','category','final_price','discount_rate','counts']

class FoodCommentListViewSerializer(serializers.ModelSerializer):
    class Meta:
        models = FoodComment
        fields = ['user','content','star']







