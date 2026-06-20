from django.contrib import admin
from django.urls import path, include
from .views import DeleteImageResource, ResourceListCreate, ResourceDetail, CategoryList, categoryList, semesterList

urlpatterns = [
    path('resources/', ResourceListCreate.as_view(), name='resource-list-create'),
    path('resources/<int:pk>/', ResourceDetail.as_view(), name='resource-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('delete-image/<int:pk>/', DeleteImageResource.as_view(), name='delete-image-resource'),
    path('semesters/', semesterList, name='semester-list'),
    path('categories/', categoryList, name='category-list'),
] 