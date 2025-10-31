from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item
from .serializers import ItemSerializer
from .filters import ItemFilter

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().prefetch_related('units')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filters and search capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ItemFilter

    # Fields that can be searched via ?search=pizza
    search_fields = ['name', 'units__unit_name']

    # Fields that can be ordered via ?ordering=price or ?ordering=-price
    ordering_fields = ['name', 'units__price']
    """
        {
        "name": "Pizza",
        "description": "Cheesy and delicious",
        "veg": true,
        "is_available": true,
        "ingredients": "Cheese, Tomato, Dough",
        "units": [
            {
            "unit_name": "Small",
            "price": 150
            },
            {
            "unit_name": "Medium",
            "price": 250
            },
            {
            "unit_name": "Large",
            "price": 350
            }
        ]
        }
    """

