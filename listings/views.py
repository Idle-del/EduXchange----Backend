from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Resource, Category
from .serializers import ResourceSerializer, CategorySerializer

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
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    
class ResourceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = 'pk'