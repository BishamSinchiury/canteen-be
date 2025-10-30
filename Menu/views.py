# Create your views here.
from django.utils.timezone import now
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Item, Transaction
from .serializers import ItemSerializer, TransactionSerializer



class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    # enable filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['veg', 'is_available']

class TransactionPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class TransactionViewSet(viewsets.ReadOnlyModelViewSet, viewsets.GenericViewSet):
    """
    Only allows list, retrieve, and create transactions.
    """
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TransactionPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'item__name',          # search by item name
        'created_by__email',   # search by user email
        'created_by__name',    # search by user name
        'created_at',          # search by date
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Optional: filter by date range using query params
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
