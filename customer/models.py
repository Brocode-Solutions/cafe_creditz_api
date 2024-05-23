from django.db import models
from django.contrib.auth.models import User
from cafe.models import Cafe


class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    total_credit = models.FloatField(default=0.0)
    total_debit = models.FloatField(default=0.0)
    last_credit_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return self.name
