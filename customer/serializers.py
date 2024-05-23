from rest_framework import serializers
from .models import Customer
from cafe.serializers import CafeSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cafe = CafeSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_code', 'name', 'email', 'phone', 'total_credit',
            'total_debit', 'last_credit_date', 'is_active', 'created_at',
            'updated_at', 'user', 'cafe'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name if instance.user else None
        response['last_name'] = instance.user.last_name if instance.user else None
        response['email'] = instance.user.email if instance.user else None
        return response
