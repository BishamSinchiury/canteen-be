# accounts/serializers.py
from rest_framework import serializers
from .models import (
    Sale, Purchase, Income, Expense,
    Creditor, Vendor, CashAccount
)
from Items.models import Item, ItemUnit
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
    # ──────── WRITE (POST) ────────
    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        write_only=True,
    )
    unit = serializers.PrimaryKeyRelatedField(
        queryset=ItemUnit.objects.all(),
        write_only=True,
    )

    # ──────── READ (GET) ────────
    item_name = serializers.CharField(source='item.name', read_only=True)
    unit_name = serializers.CharField(source='unit.unit_name', read_only=True)
    unit_price = serializers.DecimalField(
        source='unit.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    # total = price * quantity (quantity is 1 by default)
    total = serializers.SerializerMethodField()

    # Optional: full nested objects
    item_detail = ItemSerializer(source='item', read_only=True)
    unit_detail = ItemUnitSerializer(source='unit', read_only=True)

    # User info
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id',
            'item', 'unit',                    # write-only
            'item_name', 'unit_name', 'unit_price',
            'total',                           # ← NEW: per sale
            'price', 'payment_type', 'creditor',
            'created_by', 'updated_by',
            'created_at', 'updated_at',
            'item_detail', 'unit_detail'
        ]
        read_only_fields = [
            'created_by', 'updated_by', 'created_at', 'updated_at',
            'item_name', 'unit_name', 'unit_price', 'total',
            'item_detail', 'unit_detail'
        ]

    # ──────── total = price × quantity (quantity = 1 if not present) ────────
    def get_total(self, obj):
        # If you later add a `quantity` field, use it. For now: 1
        quantity = getattr(obj, 'quantity', 1)
        return (obj.price or 0) * quantity

    # ──────── AUTO-SET created_by ────────
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
  
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