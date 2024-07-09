from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CustomerViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'customer', CustomerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
