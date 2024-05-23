from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from cafe.models import Cafe
from customer.models import Customer
from staff.models import Staff
from owner.models import Owner
from cafe.serializers import CafeSerializer

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            data['user_type'] = self.get_user_type(user)
            if data['user_type'] == 'Owner':
                owner_instance = Owner.objects.get(user=user)
                cafes = Cafe.objects.filter(owner=owner_instance)
                data['user_details'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'cafes': CafeSerializer(cafes, many=True).data
                }
            elif data['user_type'] == 'Staff':
                try:
                    staff_instance = Staff.objects.get(user=user)
                    data['user_details'] = {
                        'first_name': staff_instance.user.first_name,
                        'last_name': staff_instance.user.last_name,
                        'email': staff_instance.user.email,
                        'cafe': CafeSerializer(staff_instance.cafe).data if staff_instance.cafe else None
                    }
                except Staff.DoesNotExist:
                    raise serializers.ValidationError(
                        "Staff profile not found.")
            elif data['user_type'] == 'Customer':
                try:
                    customer_instance = Customer.objects.get(user=user)
                    data['user_details'] = {
                        'first_name': customer_instance.user.first_name,
                        'last_name': customer_instance.user.last_name,
                        'email': customer_instance.user.email,
                        'cafe': customer_instance.cafe.name,
                        'total_credit': customer_instance.total_credit,
                        'total_debit': customer_instance.total_debit
                    }
                except Customer.DoesNotExist:
                    raise serializers.ValidationError(
                        "Customer profile not found.")
            else:
                data['user_details'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
            return data

        raise serializers.ValidationError("Incorrect Credentials.")

    def get_user_type(self, user):
        if hasattr(user, 'owner'):
            return 'Owner'
        if hasattr(user, 'staff'):
            return 'Staff'
        elif hasattr(user, 'customer'):
            return 'Customer'
        return 'User'


class StaffSerializer(serializers.ModelSerializer):
    cafe = CafeSerializer()

    class Meta:
        model = Staff
        fields = ('user', 'cafe')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        return response


class CustomerSerializer(serializers.ModelSerializer):
    cafe = CafeSerializer()

    class Meta:
        model = Customer
        fields = ('user', 'cafe', 'total_credit',
                  'total_debit', 'last_credit_date')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['first_name'] = instance.user.first_name
        response['last_name'] = instance.user.last_name
        response['email'] = instance.user.email
        return response


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


class UserSerializer(serializers.ModelSerializer):
    staff_details = serializers.SerializerMethodField(read_only=True)
    customer_details = serializers.SerializerMethodField(read_only=True)
    owner_details = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            'groups',
            'is_superuser',
            'staff_details',
            'customer_details',
            'owner_details',
            'user_type'
        )

    def get_staff_details(self, obj):
        try:
            staff_instance = Staff.objects.get(user=obj)
            return StaffSerializer(staff_instance).data
        except Staff.DoesNotExist:
            return None

    def get_customer_details(self, obj):
        try:
            customer_instance = Customer.objects.get(user=obj)
            return CustomerSerializer(customer_instance).data
        except Customer.DoesNotExist:
            return None

    def get_owner_details(self, obj):
        try:
            owner_instance = Owner.objects.get(user=obj)
            return OwnerSerializer(owner_instance).data
        except Owner.DoesNotExist:
            return None

    def get_user_type(self, obj):
        if hasattr(obj, 'owner'):
            return 'Owner'
        if hasattr(obj, 'staff'):
            return 'Staff'
        elif hasattr(obj, 'customer'):
            return 'Customer'
        return 'User'
