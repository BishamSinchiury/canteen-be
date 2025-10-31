from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item, NonFood
from .serializers import ItemSerializer, NonFoodSerializer
from .filters import ItemFilter
import re

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().prefetch_related('units')
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    # Add filters and search capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ItemFilter

    # Fields that can be searched via ?search=pizza
    search_fields = ['name', 'units__unit_name']

    # Fields that can be ordered via ?ordering=price or ?ordering=-price
    ordering_fields = ['name', 'units__price']
   
class NonFoodViewSet(viewsets.ModelViewSet):
    queryset = NonFood.objects.all()
    serializer_class = NonFoodSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']

