from rest_framework import serializers
from .models import Item, ItemUnit, NonFood
import json
import re

class ItemUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUnit
        fields = ['id', 'unit_name', 'price']

class ItemSerializer(serializers.ModelSerializer):
    units = ItemUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'veg', 'image',
            'is_available', 'ingredients', 'units'
        ]

    def get_units_data(self, validated_data):
        request = self.context.get('request')
        if request and request.content_type.startswith('multipart/form-data'):
            data = request.data
            units = []
            unit_pattern = re.compile(r'units\[(\d+)\]\[(unit_name|price)\]')

            temp_units = {}
            for key, value in data.items():
                match = unit_pattern.match(key)
                if match:
                    index = int(match.group(1))
                    field = match.group(2)
                    if index not in temp_units:
                        temp_units[index] = {}
                    if isinstance(value, (list, tuple)):
                        value = value[0]
                    temp_units[index][field] = value

            for index in sorted(temp_units.keys()):
                unit = temp_units[index]
                if 'price' in unit:
                    try:
                        unit['price'] = float(unit['price'])
                    except ValueError:
                        unit['price'] = 0
                units.append(unit)
            return units
        else:
            return validated_data.pop('units', [])

    def create(self, validated_data):
        units_data = self.get_units_data(validated_data)
        item = Item.objects.create(**validated_data)
        for unit in units_data:
            ItemUnit.objects.create(item=item, unit_name=unit["unit_name"], price=unit["price"])
        return item

    def update(self, instance, validated_data):
        units_data = self.get_units_data(validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if units_data is not None:
            instance.units.all().delete()
            for unit in units_data:
                ItemUnit.objects.create(item=instance, **unit)

        return instance


class NonFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonFood
        fields = [
            'id',
            'name',
            'description',
            'is_available',
            'price',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
