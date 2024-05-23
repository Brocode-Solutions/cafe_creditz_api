from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from staff.models import Staff
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'staff'):
            staff = Staff.objects.get(user=user)
            return Transaction.objects.filter(cafe=staff.cafe)
        elif hasattr(user, 'owner'):
            cafe_id = self.request.headers.get('cafe_id')
            if cafe_id:
                return Transaction.objects.filter(cafe_id=cafe_id)
            else:
                return Transaction.objects.filter(cafe__owner=user.owner)
        else:
            return Transaction.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
