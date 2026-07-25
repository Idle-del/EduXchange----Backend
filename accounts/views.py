from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.utils import generate_password_reset_token, send_password_reset_email
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import EmailTokenObtainPairSerializer
from .permissions import IsOwner
from rest_framework.decorators import APIView, api_view
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
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        
        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "bio": user.bio,
            "semester": user.semester,
            "department": user.department,
            "profile_picture": (
                user.profile_picture.url
                if user.profile_picture else None
            )
        })
    
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
    
@api_view(['POST'])
def forget_password(request):
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
        user.reset_password_token = generate_password_reset_token()
        
        # Temporarily commented out the email sending for testing purposes
        # send_password_reset_email(user.email, user.reset_password_token)
        
        user.save()
        return Response({"message": "Password reset instructions sent to your email."}, status=200)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=400)
    

def reset_password(request, token):
    try:
        user = CustomUser.objects.get(reset_password_token=token)

    except CustomUser.DoesNotExist:
        return render(
            request,
            "reset_success.html",
            {
                "success": False,
                "message": "This password reset link is invalid or has already been used."
            }
        )

    if request.method == "GET":
        return render(
            request,
            "reset_password.html",
            {
                "token": token
            }
        )

    password = request.POST.get("password")
    confirm = request.POST.get("confirm")

    if not password:
        return render(
            request,
            "reset_password.html",
            {
                "token": token,
                "error": "Password is required."
            }
        )

    if len(password) < 8:
        return render(
            request,
            "reset_password.html",
            {
                "token": token,
                "error": "Password must be at least 8 characters."
            }
        )

    if password != confirm:
        return render(
            request,
            "reset_password.html",
            {
                "token": token,
                "error": "Passwords do not match."
            }
        )

    user.set_password(password)
    user.reset_password_token = None
    user.save()

    return render(
        request,
        "reset_successful.html",
        {
            "success": True,
            "message": "Your password has been changed successfully."
        }
    )