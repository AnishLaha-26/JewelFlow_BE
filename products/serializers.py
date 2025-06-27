from rest_framework import serializers
from .models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        Validate that the category name is unique (case-sensitive)
        """
        
        if self.instance and self.instance.name.lower() == value.lower():
            return value
        
        if ProductCategory.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

