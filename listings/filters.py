import django_filters
from .models import Resource

class ResourceFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category', lookup_expr='exact')
    semester = django_filters.NumberFilter(field_name='semester', lookup_expr='exact')
    type = django_filters.ChoiceFilter(field_name='type', choices=Resource.type_choices)

    class Meta:
        model = Resource
        fields = ['category', 'semester', 'type']