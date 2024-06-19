from rest_framework.routers import DefaultRouter
from rest_framework import viewsets,permissions
from .models import  Cafe
from .serializers import CafeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'owner')
    
class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    '''def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner, created_by=self.request.user)'''
    @action(detail=False, methods=['post'], url_path='create_cafe')
    def create_cafe(self, request):
        owner = request.user.owner
        data = request.data.copy()
        data['owner'] = owner.id
        data['created_by'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, owner=owner)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

