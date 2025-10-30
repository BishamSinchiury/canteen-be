from rest_framework import serializers
from .models import Item
from .models import Transaction


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

from rest_framework import serializers
from .models import Transaction
from User.models import User
from Menu.models import Item  # adjust import if needed

class TransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  # display user email/name
    item = serializers.StringRelatedField()  # display item name

    class Meta:
        model = Transaction
        fields = ['id', 'item', 'quantity', 'total_price', 'created_at', 'created_by']
        read_only_fields = ['total_price', 'created_at', 'created_by']

    def create(self, validated_data):
        # Assign logged-in user automatically
        user = self.context['request'].user
        transaction = Transaction.objects.create(created_by=user, **validated_data)
        return transaction
