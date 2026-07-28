import cloudinary
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from .models import Resource, Category, ResourceImage, Favorite
from .serializers import ResourceSerializer, CategorySerializer, ResourceImageSerializer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ResourceFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsResourceImageOwnerOrReadOnly
from rest_framework.response import Response

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
    
@api_view(['GET'])
def semesterList(request):
    semesters = [
        {'id': value, 'name': label} for value, label in Resource.semester_choices
    ]
    return Response(semesters)

@api_view(['GET'])
def statusList(request):
    statuses = [
        {'id': value, 'name': label} for value, label in Resource.status_choices
    ]
    return Response(statuses)

@api_view(['GET'])
def typeList(request):
    types = [
        {'id': value, 'name': label} for value, label in Resource.type_choices
    ]
    return Response(types)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def userResources(request):
#     resources = Resource.objects.filter(
#         uploaded_by=request.user
#     ).order_by('-created_at')

#     serializer = ResourceSerializer(
#         resources,
#         many=True,
#         context={'request': request},
#     )

#     return Response(serializer.data)

class UserResources(ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Resource.objects.filter(uploaded_by=user).order_by('-created_at')
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addFavorite(request, pk):

    resource = Resource.objects.get(id=pk)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        resource=resource
    )

    if not created:
        return Response(
            {"message":"Already added to favorites"},
            status=status.HTTP_400_BAD_REQUEST
        )


    return Response(
        {"message":"Added to favorites"},
        status=status.HTTP_201_CREATED
    )
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeFavorite(request, pk):

    try:
        favorite = Favorite.objects.get(
            user=request.user,
            resource_id=pk
        )

        favorite.delete()

        return Response(
            {"message":"Removed from favorites"},
            status=status.HTTP_200_OK
        )


    except Favorite.DoesNotExist:

        return Response(
            {"message":"Favorite not found"},
            status=status.HTTP_404_NOT_FOUND
        )
        
class UserFavorites(ListAPIView):

    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Resource.objects.filter(
            favorited_by__user=self.request.user
        ).order_by('-favorited_by__created_at')