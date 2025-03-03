from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework.views import APIView

from django.db.models import Q
from .models import Store
from .serializers import StoreListViewSerializer


class StoreListView(APIView):
    def get(self, request, city=None, store_type=None, is_store_open=None, is_post_free=None, search=None):
        filters = Q()  # a empty query
        query_params = {
            'city': request.query_params.get('city', None),
            'store_type': request.query_params.get('store_type', None),
            'is_store_open': request.query_params.get('is_store_open', None),
            'is_post_free': request.query_params.get('is_post_free', None),
        }


        for key, value in query_params.items():
            if value is not None:
                filters &= Q(**{key: value})

        search = request.query_params.get('serach',None)
        if search is not None:
            filters &= Q(name__icontains = request.query_params['search'])

        stores = Store.objects.filter(filters)

        paginator = pagination.PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)  # Default page size is 10
        paginated_stores = paginator.paginate_queryset(stores, request)
        serializer = StoreListViewSerializer(paginated_stores, many=True)
        return paginator.get_paginated_response(serializer.data)



