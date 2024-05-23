from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import StaffViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'', StaffViewSet)

urlpatterns = [
    path('api/staff', include(router.urls)),
]
