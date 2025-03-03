from django.urls import path,include
from .views import StoreListView,FoodCommentListView,FoodListView
urlpatterns = [
    ('api/stores',StoreListView.as_view()),
    ('api/foods',FoodListView.as_view()),
    ('api/foods/<int:pk>/comments',FoodCommentListView.as_view()),
]