from rest_framework import serializers
from django.db import transaction
from .models import Resource, Category, ResourceImage, Favorite

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
    is_favorite = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()
    extra_images = ResourceImageSerializer(many=True, read_only=True)
    file = serializers.FileField(required=False, allow_null=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True), write_only=True, required=False)
    class Meta:
        model = Resource
        fields = ['id','status', 'title', 'description', 'file', 'image','extra_images','uploaded_images', 'category', 'category_name', 'uploaded_by', 'semester', 'semester_name', 'uploaded_by_name', 'created_at', 'updated_at', 'type', 'price', 'is_favorite', 'favorite_count']
        
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']
        
    def save_uploaded_images(self, resource, uploaded_images):
        for image in uploaded_images:
            ResourceImage.objects.create(resource=resource, image=image)
        
    @transaction.atomic
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        resource = Resource.objects.create(**validated_data)
        
        self.save_uploaded_images(resource, uploaded_images)
        return resource
    
    @transaction.atomic
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        validated_data.pop('type', None)  # Prevent updating the type field
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self.save_uploaded_images(instance, uploaded_images)
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
        return obj.uploaded_by.get_full_name() if obj.uploaded_by else None      
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.file:
            representation['file'] = instance.file.build_url(secure=True)
        else:
            representation['file'] = None
        return representation      
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            # Check if favorited_by cache/prefetch is present or fallback to DB query
            if hasattr(obj, '_prefetched_objects_cache') and 'favorited_by' in obj._prefetched_objects_cache:
                return any(fav.user_id == request.user.id for fav in obj.favorited_by.all())
            return Favorite.objects.filter(
                user=request.user,
                resource=obj
            ).exists()
        return False

    def get_favorite_count(self, obj):
        if hasattr(obj, 'favorite_count_annotated'):
            return obj.favorite_count_annotated
        if hasattr(obj, '_prefetched_objects_cache') and 'favorited_by' in obj._prefetched_objects_cache:
            return len(obj.favorited_by.all())
        return obj.favorited_by.count()
    
class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = [
            'id',
            'resource',
            'created_at'
        ]