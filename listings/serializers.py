from rest_framework import serializers
from .models import Resource, Category, ResourceImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ResourceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceImage
        fields = ['id', 'image']
        
class ResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    semester_name = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()
    extra_images = ResourceImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True), write_only=True, required=False)
    class Meta:
        model = Resource
        fields = ['id','status', 'title', 'description', 'file', 'image','extra_images','uploaded_images', 'category', 'category_name', 'uploaded_by', 'semester', 'semester_name', 'uploaded_by_name', 'created_at', 'updated_at', 'type', 'price']
        
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        resource = Resource.objects.create(**validated_data)
        
        for image in uploaded_images:
            ResourceImage.objects.create(resource=resource, image=image)
        return resource
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for image in uploaded_images:
            ResourceImage.objects.create(resource=instance, image=image)
        return instance

    def validate(self, attrs):
        file = attrs.get('file', getattr(self.instance, 'file', None))
        image = attrs.get('image', getattr(self.instance, 'image', None))
        uploaded_images = attrs.get('uploaded_images', [])
        resource_type = attrs.get('type', getattr(self.instance, 'type', None))
        price = attrs.get('price', getattr(self.instance, 'price', None))
        
        if not file and not image and not uploaded_images:
            raise serializers.ValidationError('Either a file or an image is required.')
        
        if resource_type == 'sell':
            if not price or price <= 0:
                raise serializers.ValidationError({
                    'price': 'Price must be a positive number for resources that are for sale.'
                })
        else:
            attrs['price'] = None
        return attrs

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_semester_name(self, obj):
        return obj.get_semester_display() if obj.semester else None
    
    def get_uploaded_by_name(self, obj):
        # return f'{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}' if obj.uploaded_by else None 
        return obj.uploaded_by.get_full_name() if obj.uploaded_by else None            