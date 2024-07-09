from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        print(request.data)
        print(request.data['user'])
        user_type=request.get_user_type()
        print(user_type)
        if user_type !='Staff':
            return Response({"detail": "Only staff can create customers"}, status=status.HTTP_403_FORBIDDEN)       
        cafe_id = request.get_cafe()
        if cafe_id is None:
             return Response({"message": "Cafe  not found in request."}, status=status.HTTP_400_BAD_REQUEST)
        user_data = request.data.pop('user')


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Pass user data and cafe_id to the serializer
        serializer.save(user=user_data, cafe_id=cafe_id)       
        print("serializer")
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
