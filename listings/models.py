from django.db import models
from django.conf import settings
import os

from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    
class Resource(models.Model):
    
    # Choices for the semester field
    semester_choices = [
       (1, 'Semester 1'),
       (2, 'Semester 2'),
        (3, 'Semester 3'),
         (4, 'Semester 4'),
         (5, 'Semester 5'),
         (6, 'Semester 6'),
         (7, 'Semester 7'),
         (8, 'Semester 8'),
    ]
    type_choices = [
        ('free', 'Free'),
        ('lend', 'Lend'),
        ('sell', 'Sell'),
    ]
    status_choices = [
        ('available', 'Available'),
        ('lent', 'Lent'),
        ('sold', 'Sold'),
    ]
    
    status = models.CharField(max_length=10, choices=status_choices, default='available')
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    type = models.CharField(max_length=10, choices=type_choices, default='free')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    
    file = CloudinaryField(
    resource_type="raw",
    blank=True,
    null=True,
)
    
    image = models.ImageField(upload_to='resource_images/', null=True, blank=True) # New field for resource image
        
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='resources') # Each resource belongs to a category
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources', null=True, blank=True) # Each resource is uploaded by a user
    
    semester = models.IntegerField(choices=semester_choices, blank=True, null=True) # Semester field with choices from 1 to 8
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class ResourceImage(models.Model):
    resource = models.ForeignKey(Resource, related_name='extra_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resource_images/')
    
    def __str__(self):
        return f"Image for {self.resource.title}"
    
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        return f"{self.user.email} favorite {self.resource.title}"