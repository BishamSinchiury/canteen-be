# accounts/admin.py
from django.contrib import admin
from .models import (
    Creditor, Vendor, CashAccount,
    Sale, Purchase, Income, Expense
)

# --------------------------
# Inline for Item Units (if needed elsewhere)
# --------------------------

# --------------------------
# Creditor Admin
# --------------------------
@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_balance', 'contact_no', 'description_preview')
    list_filter = ('account_balance',)
    search_fields = ('name', 'contact_no', 'description')
    fields = ('name', 'description', 'account_balance', 'contact_no')

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'


# --------------------------
# Vendor Admin
# --------------------------
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_balance', 'contact_no', 'description_preview')
    list_filter = ('account_balance',)
    search_fields = ('name', 'contact_no', 'description')
    fields = ('name', 'description', 'account_balance', 'contact_no')

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'


# --------------------------
# Cash Account (Singleton)
# --------------------------
@admin.register(CashAccount)
class CashAccountAdmin(admin.ModelAdmin):
    list_display = ('balance',)
    readonly_fields = ('balance',)

    def has_add_permission(self, request):
        # Allow only one instance
        return not CashAccount.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion


# --------------------------
# Sale Admin
# --------------------------
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit', 'price', 'payment_type', 'creditor', 'created_by', 'created_at')
    list_filter = ('payment_type', 'created_at', 'created_by', 'creditor')
    search_fields = ('item__name', 'unit__unit_name', 'creditor__name', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at', 'price')  # Price auto-filled
    autocomplete_fields = ('item', 'unit', 'creditor', 'created_by', 'updated_by')

    fieldsets = (
        ('Sale Details', {
            'fields': ('item', 'unit', 'price', 'payment_type', 'creditor')
        }),
        ('Audit', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'item', 'unit', 'creditor', 'created_by', 'updated_by'
        )


# --------------------------
# Purchase Admin
# --------------------------
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit', 'price', 'payment_type', 'vendor', 'created_by', 'created_at')
    list_filter = ('payment_type', 'created_at', 'created_by', 'vendor')
    search_fields = ('item__name', 'unit__unit_name', 'vendor__name', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at', 'price')
    autocomplete_fields = ('item', 'unit', 'vendor', 'created_by', 'updated_by')

    fieldsets = (
        ('Purchase Details', {
            'fields': ('item', 'unit', 'price', 'payment_type', 'vendor')
        }),
        ('Audit', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'item', 'unit', 'vendor', 'created_by', 'updated_by'
        )


# --------------------------
# Income Admin
# --------------------------
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description_preview', 'sale', 'creditor_payment', 'created_at')
    list_filter = ('created_at', 'sale', 'creditor_payment')
    search_fields = ('description', 'sale__item__name', 'creditor_payment__name')
    autocomplete_fields = ('sale', 'creditor_payment')

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sale', 'creditor_payment')


# --------------------------
# Expense Admin
# --------------------------
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description_preview', 'purchase', 'vendor_payment', 'created_at')
    list_filter = ('created_at', 'purchase', 'vendor_payment')
    search_fields = ('description', 'purchase__item__name', 'vendor_payment__name')
    autocomplete_fields = ('purchase', 'vendor_payment')

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('purchase', 'vendor_payment')