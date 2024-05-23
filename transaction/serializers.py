from rest_framework import serializers
from .models import Transaction
from customer.models import Customer
from customer.serializers import CustomerSerializer


class TransactionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'customer', 'transaction_type',
            'created_by', 'created_at', 'updated_at', 'cafe', 'is_active'
        ]
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'cafe')

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        customer_id = customer_data.get('id')

        if customer_id:
            customer = Customer.objects.get(id=customer_id)
        else:
            customer = Customer.objects.create(**customer_data)

        transaction = Transaction.objects.create(
            customer=customer, **validated_data)

        if transaction.transaction_type == 'credit':
            customer.total_credit += transaction.amount
            customer.last_credit_date = transaction.created_at
        elif transaction.transaction_type == 'debit':
            customer.total_debit += transaction.amount

        customer.save()
        return transaction
