from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
def resource_file_path(instance, filename):
    category_name = instance.category.name.replace(' ', '_') # Replace spaces with underscores for better file paths
    
    return f'resources/{category_name}/{filename}'
    
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
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    file = models.FileField(upload_to=resource_file_path) # Files uploaded by users will be stored in the 'resources/' directory
    
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='resources') # Each resource belongs to a category
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources', null=True, blank=True) # Each resource is uploaded by a user
    
    semester = models.IntegerField(choices=semester_choices) # Semester field with choices from 1 to 8
    
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for when the resource was created
    updated_at = models.DateTimeField(auto_now=True) # Timestamp for when the resource was last updated
    
    def __str__(self):
        return self.title