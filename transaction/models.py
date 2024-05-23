from django.db import models
from customer.models import Customer
from django.contrib.auth.models import User


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    amount = models.FloatField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=6, choices=TRANSACTION_TYPES)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cafe = models.ForeignKey(
        'cafe.Cafe', on_delete=models.CASCADE, related_name='transactions')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} for {self.customer.name}'
