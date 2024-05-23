from django.contrib.auth.models import User
from django.db import models
from owner.models import Owner


class Cafe(models.Model):
    name = models.CharField(max_length=255)
    address_first_line = models.CharField(max_length=255)
    email = models.EmailField()
    primary_phone_mobile = models.CharField(max_length=20)
    # Comma-separated or newline-separated numbers
    other_contact_numbers = models.TextField(blank=True, null=True)
    phone_landline = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='cafe_logos/', blank=True, null=True)
    translation_required = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_box_number = models.CharField(max_length=50, blank=True, null=True)
    # Comma-separated or newline-separated services
    services = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    total_customers = models.PositiveIntegerField(
        default=0, verbose_name="total_customers")
    total_credit = models.PositiveIntegerField(
        default=0, verbose_name="total_credit")
    total_debit = models.PositiveIntegerField(
        default=0, verbose_name="total_debit")
    total_transactions = models.PositiveIntegerField(
        default=0, verbose_name="total_transactions")
    transaction_statistics = models.JSONField(
        default=list, blank=True, null=True)
    credit_statistics = models.JSONField(default=list, blank=True, null=True)
    customer_statistics = models.JSONField(default=list, blank=True, null=True)
    debit_statistics = models.JSONField(default=list, blank=True, null=True)

    # Default fields
    created_by = models.ForeignKey(
        User, related_name="cafe_created", on_delete=models.SET_NULL,
        null=True)
    updated_by = models.ForeignKey(
        User, related_name="cafe_updated", on_delete=models.SET_NULL,
        null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='owned_cafes')

    def __str__(self):
        return self.name
