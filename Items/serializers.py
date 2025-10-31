from rest_framework import serializers
from .models import Item, ItemUnit

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUnit
        fields = ['id', 'unit_name', 'price']