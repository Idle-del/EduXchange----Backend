from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomUserRetrieveUpdateDestroyView, EmailTokenObtainPairView, CustomUserCreateView, UserProfile, verify_email

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profile/', CustomUserRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
    path('user/<int:pk>/', UserProfile.as_view(), name='user-list'),
    path('verify-email/<token>/', verify_email, name='verify-email'),
]