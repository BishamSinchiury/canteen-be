# accounts/serializers.py
from rest_framework import serializers
from .models import (
    Sale, Purchase, Income, Expense,
    Creditor, Vendor, CashAccount
)
from Items.serializers import ItemSerializer, ItemUnitSerializer
from User.serializers import UserSerializer

# --------------------------
# Creditor / Vendor
# --------------------------
class CreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creditor
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

# --------------------------
# Cash Account
# --------------------------
class CashAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashAccount
        fields = '__all__'

# --------------------------
# Sale / Purchase
# --------------------------
class SaleSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    unit = ItemUnitSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    creditor = CreditorSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    unit = ItemUnitSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'

# --------------------------
# Income / Expense
# --------------------------
class IncomeSerializer(serializers.ModelSerializer):
    sale = SaleSerializer(read_only=True)
    creditor_payment = CreditorSerializer(read_only=True)

    class Meta:
        model = Income
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer(read_only=True)
    vendor_payment = VendorSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'

class SimpleCreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creditor
        fields = ['id', 'name']

class SimpleVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name']