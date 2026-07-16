from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import EmailTokenObtainPairSerializer
from .permissions import IsOwner
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
class CustomUserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = []  # Allow anyone to create an account

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    
class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_object(self):
        return self.request.user
    
@api_view(['GET'])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_token=token)
        user.is_verified= True
        user.email_token = None
        user.save()
        print(f"User {user.email} has been verified.")
        
        return Response({"message": "Email verified successfully."}, status=200)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid token."}, status=400)