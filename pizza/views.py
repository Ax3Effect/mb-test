from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets

from pizza.models import AnonymousCustomer, MenuItemSize, MenuItem
from pizza.models import Order, OrderItem, OrderItemSize

from pizza.serializers import MenuItemSerializer, MenuItemSizeSerializer
# Create your views here.

'''
class CreateOrderView(APIView):
    def post(self, request, format=None):
'''

class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

