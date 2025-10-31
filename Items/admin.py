# items/admin.py
from django.contrib import admin
from .models import Item, ItemUnit


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'veg', 'is_available', 'display_units')
    list_filter = ('veg', 'is_available')
    search_fields = ('name', 'description', 'ingredients')
    readonly_fields = ('id',)

    def display_units(self, obj):
        """Display a comma-separated list of unit names and prices."""
        return ", ".join([f"{unit.unit_name} ({unit.price})" for unit in obj.units.all()])
    display_units.short_description = 'Available Units'


@admin.register(ItemUnit)
class ItemUnitAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit_name', 'price')
    list_filter = ('item__veg', 'item__is_available')
    search_fields = ('item__name', 'unit_name')
    readonly_fields = ('id',)