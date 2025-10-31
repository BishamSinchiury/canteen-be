# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SaleViewSet, PurchaseViewSet,
    IncomeViewSet, ExpenseViewSet,
    CreditorViewSet, VendorViewSet, CashAccountViewSet
)

router = DefaultRouter()
router.register(r'sales', SaleViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'creditors', CreditorViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'cash', CashAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
