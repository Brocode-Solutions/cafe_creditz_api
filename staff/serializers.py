from rest_framework import serializers
from .models import Staff
from cafe.serializers import CafeSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cafe = CafeSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = [
            'user', 'phone_number', 'address', 'date_of_birth',
            'designation', 'cafe'
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        return response
