from rest_framework import serializers
from pizza.models import *

class MenuItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemSize
        fields = ('id', 'name', 'price')

class MenuItemSerializer(serializers.ModelSerializer):
    size = MenuItemSizeSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'