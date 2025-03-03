from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.views import APIView

from django.db.models import Q
from .models import Store,Food
from .serializers import StoreListViewSerializer,FoodListViewSerializer

def get_filter_query_params(request,*query_params) -> Q():
    '''get the query params and return the filters should apply
    if query_param is none the filter for that not applied'''
    filters = Q()
    query_params_map = dict()
    for query_param in query_params:
        query_params_map[query_param] = request.query_params.get(query_param,None)
    for key , value in query_params_map.items():
        if value is not None:
            filters &= Q(**{key : value})
    return filters

class StoreListView(APIView):
    def get(self, request, city=None, store_type=None, is_store_open=None, is_post_free=None, search=None):
        filters = get_filter_query_params(request,city,store_type,is_store_open,is_post_free)

        search = request.query_params.get('serach',None)
        if search is not None:
            filters &= Q(name__icontains = request.query_params['search'])

        stores = Store.objects.filter(filters,is_active = True)

        paginator = pagination.PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)  # Default page size is 10
        paginated_stores = paginator.paginate_queryset(stores, request)
        serializer = StoreListViewSerializer(paginated_stores, many=True)
        return paginator.get_paginated_response(serializer.data)

class FoodListView(APIView):
    def get(self,request, store = None, category = None , has_discount = None , is_available = None , order = None):
        #order have values of price or discount.
        filters = get_filter_query_params(request,store , category,has_discount,is_available)

        if order == 'price':
            foods = Food.objects.filter(filters).order_by('final_price')
        elif order=='discount':
            foods = Food.objects.filter(filters).order_by('discount_rate')
        else:
            foods = Food.objects.filter(filters)

        serializer = FoodListViewSerializer(foods , many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)




