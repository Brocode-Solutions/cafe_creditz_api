from rest_framework import serializers
from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['user', 'phone_number', 'address',
                  'date_of_birth', 'designation']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        return response
