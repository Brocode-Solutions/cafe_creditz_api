from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cafe.api import CafeViewSet

# Create a DefaultRouter instance
router = DefaultRouter()
router.register(r'api/cafe', CafeViewSet, basename='cafe')

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered with the router
]