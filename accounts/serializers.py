from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name','profile_picture', 'last_name', 'bio', 'department', 'semester']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = CustomUser.objects.filter(email=email).first()
        
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')
        
        data = super().validate({
            'email': user.email,
            'password': password
        })
        
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['id'] = user.id
        data['profile_picture'] = user.profile_picture.url if user.profile_picture else None
        data['bio'] = user.bio
        data['department'] = user.department
        data['semester'] = user.semester
        
        return data