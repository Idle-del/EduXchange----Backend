from django.contrib import admin
from django.urls import path, include
from .views import ResourceListCreate, ResourceDetail

urlpatterns = [
    path('resources/', ResourceListCreate.as_view(), name='resource-list-create'),
    path('resources/<int:pk>/', ResourceDetail.as_view(), name='resource-detail'),
] 