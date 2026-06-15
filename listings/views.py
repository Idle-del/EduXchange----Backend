from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from .models import Resource, Category, ResourceImage
from .serializers import ResourceSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ResourceFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsResourceImageOwnerOrReadOnly

# Create your views here.

## Function-based View

# @api_view(['GET'])
# def resource_list(request):
#     resources = Resource.objects.all()
    
#     serializer = ResourceSerializer(resources, many=True)
    
#     return Response(serializer.data)

## APIView-based View

# class ResourceList(APIView):
#     def get(self, request):
#         resources = Resource.objects.all()
        
#         serializer = ResourceSerializer(resources, many=True)
        
#         return Response(serializer.data, status=status.HTTP_200_OK)

## GenericAPIView-based View

# class ResourceList(GenericAPIView):
#     queryset = Resource.objects.all()
#     serializer_class = ResourceSerializer
    
#     def get(self, request):
#         resources = self.get_queryset()
#         serializer = self.get_serializer(resources, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ResourceListCreate(ListCreateAPIView):
    queryset = Resource.objects.all().order_by('-created_at')
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResourceFilter
    search_fields = ['title', 'description', 'category__name']
    ordering_fields = ['created_at', 'updated_at', 'title']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
class ResourceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    pagination_class = None  # Disable pagination for categories
    
class DeleteImageResource(DestroyAPIView):
    queryset = ResourceImage.objects.all()
    permission_classes = [IsAuthenticated, IsResourceImageOwnerOrReadOnly]