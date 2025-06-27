from django.db import models
from django.utils import timezone


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Product Category"
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
