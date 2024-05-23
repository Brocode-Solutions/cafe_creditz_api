from rest_framework import serializers
from .models import Cafe
from owner.serilaizers import OwnerSerializer


class CafeSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Cafe
        fields = [
            'id', 'name', 'address_first_line', 'email',
            'primary_phone_mobile', 'other_contact_numbers', 'phone_landline',
            'logo', 'translation_required',
            'country', 'city', 'post_box_number', 'services', 'is_active',
            'total_customers', 'total_credit', 'total_debit',
            'total_transactions', 'transaction_statistics',
            'credit_statistics', 'customer_statistics',
            'debit_statistics', 'created_by',
            'updated_by', 'created_on',
            'updated_on', 'owner'
        ]
        read_only_fields = ('created_by', 'updated_by',
                            'created_on', 'updated_on', 'owner')

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['created_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)
