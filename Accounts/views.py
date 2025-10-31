# accounts/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sale, Purchase, Income, Expense, Creditor, Vendor, CashAccount
from .serializers import (
    SaleSerializer, PurchaseSerializer,
    IncomeSerializer, ExpenseSerializer,
    CreditorSerializer, VendorSerializer,
    CashAccountSerializer
)

# --------------------------
# Creditor / Vendor / Cash
# --------------------------
class CreditorViewSet(viewsets.ModelViewSet):
    queryset = Creditor.objects.all()
    serializer_class = CreditorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'contact_no']
    filterset_fields = ['account_balance']
    ordering_fields = ['name', 'account_balance']

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'contact_no']
    filterset_fields = ['account_balance']
    ordering_fields = ['name', 'account_balance']

class CashAccountViewSet(viewsets.ModelViewSet):
    queryset = CashAccount.objects.all()
    serializer_class = CashAccountSerializer

# --------------------------
# Sale / Purchase
# --------------------------
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().select_related('item', 'unit', 'created_by', 'updated_by', 'creditor')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item__name', 'unit__unit_name', 'created_by__username', 'creditor__name']
    filterset_fields = ['payment_type', 'creditor', 'created_at', 'updated_at']
    ordering_fields = ['price', 'created_at', 'updated_at']

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().select_related('item', 'unit', 'created_by', 'updated_by', 'vendor')
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item__name', 'unit__unit_name', 'created_by__username', 'vendor__name']
    filterset_fields = ['payment_type', 'vendor', 'created_at', 'updated_at']
    ordering_fields = ['price', 'created_at', 'updated_at']

# --------------------------
# Income / Expense
# --------------------------
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all().select_related('sale', 'creditor_payment')
    serializer_class = IncomeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'sale__item__name', 'creditor_payment__name']
    filterset_fields = ['created_at', 'sale', 'creditor_payment', 'amount']
    ordering_fields = ['amount', 'created_at']

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().select_related('purchase', 'vendor_payment')
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'purchase__item__name', 'vendor_payment__name']
    filterset_fields = ['created_at', 'purchase', 'vendor_payment', 'amount']
    ordering_fields = ['amount', 'created_at']
