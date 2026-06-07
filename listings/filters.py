import django_filters
from .models import Resource

class ResourceFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category', lookup_expr='exact')
    semester = django_filters.NumberFilter(field_name='semester', lookup_expr='exact')
    
    class Meta:
        model = Resource
        fields = ['category', 'semester']