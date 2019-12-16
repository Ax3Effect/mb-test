from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.decorators import action

from pizza.models import AnonymousCustomer, MenuItemSize, MenuItem
from pizza.models import Order, OrderItem, OrderItemSize

from pizza.serializers import MenuItemSerializer, MenuItemSizeSerializer
from pizza.serializers import OrderReadSerializer, OrderWriteSerializer
# Create your views here.

'''
class CreateOrderView(APIView):
    def post(self, request, format=None):
'''

class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Order.objects.get_queryset().order_by('id')
    serializer_class = OrderReadSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return OrderReadSerializer
        elif self.action == "create" or self.action == "update":
            return OrderWriteSerializer
        return OrderReadSerializer
    
    def create(self, request):
        order_serializer = OrderWriteSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        order_id = get_object_or_404(Order, pk=pk)
        order_serializer = OrderWriteSerializer(order_id, data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        order = self.get_object()
        r = order.set_status(request.data["status"])
        if r:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)