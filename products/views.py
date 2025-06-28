from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ProductCategory
from .serializers import ProductCategorySerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only allow admins users to edit categories
    """
    def has_permission(self, request, view):
        #Read permissions are allowed to any request, so allow GET, HEAD, OPTIONS always
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product categories
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'
    
    def get_queryset(self):
        """
        Optionally filter the queryset by is_active
        """
        queryset = ProductCategory.objects.all()
        is_active = self.request.query_params.get('is_active',None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset
    
    def perform_create(self, serializer):
        """
        Set create_by field to the current user
        """
        serializer.save()
    
    def perform_update(self, serializer):
        """
        Set update_at timestamp when updating
        """
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle the is_active status of a category
        """
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        return Response({'status': 'active' if category.is_active else 'inactive'})
  



class BulkDeleteCategoriesView(views.APIView):
    """
    API View for bulk deleting product categories
    """
    permission_classes = [IsAdminOrReadOnly]
    
    def delete(self, request):
        """
        Delete multiple categories at once
        Expected payload: {"ids": [1, 2, 3]}
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {"error": "No IDs provided. Please provide a list of category IDs to delete."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert string IDs to integers
        try:
            ids = [int(id_val) for id_val in ids]
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid ID format. IDs must be integers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if all categories exist
        existing_ids = set(ProductCategory.objects.filter(id__in=ids).values_list('id', flat=True))
        non_existing_ids = set(ids) - existing_ids
        
        if non_existing_ids:
            return Response(
                {"error": f"Categories with these IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete the categories
        deleted_count, _ = ProductCategory.objects.filter(id__in=ids).delete()
        
        return Response(
            {"message": f"Successfully deleted {deleted_count} categories"},
            status=status.HTTP_200_OK
        )