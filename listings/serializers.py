from rest_framework import serializers
from .models import Resource, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class ResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    semester_name = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'file', 'category', 'category_name', 'uploaded_by', 'semester', 'semester_name', 'uploaded_by_name', 'created_at', 'updated_at']
        
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_semester_name(self, obj):
        return obj.get_semester_display() if obj.semester else None
    
    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.username if obj.uploaded_by else None

    