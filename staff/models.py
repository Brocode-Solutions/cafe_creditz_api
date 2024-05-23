from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    cafe = models.ForeignKey('cafe.Cafe', on_delete=models.CASCADE,
                             related_name='staff_members',
                             null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} ({self.cafe.name})'
