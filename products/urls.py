from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', views.ProductCategoryViewSet, basename='product-category')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('categories/bulk/', views.BulkDeleteCategoriesView.as_view(), name='bulk-delete-categories'),
    path('', include(router.urls)),
]

