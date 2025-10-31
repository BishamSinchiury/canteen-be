# filters.py
import django_filters
from .models import Item, ItemUnit

class ItemFilter(django_filters.FilterSet):
    # Filter by price through related ItemUnit
    price = django_filters.NumberFilter(field_name="units__price", lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name="units__price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="units__price", lookup_expr='lte')

    unit_name = django_filters.CharFilter(field_name="units__unit_name", lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['name', 'veg', 'is_available', 'price', 'min_price', 'max_price', 'unit_name']
