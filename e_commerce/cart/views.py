from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from products.models import ProductItem
from rest_framework import status
from products.serializers import ProductItemSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()
    items = []
    for item in cart_items:
        serializer = ProductItemSerializer(item.product)
        product_data = serializer.data
        item_data = {
            'id': item.id,
            'product': product_data,
            'quantity': item.quantity,
            'total_price': item.total_price
        }
        items.append(item_data)
    return Response(items)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id or not quantity:
        return Response({'error': 'Product ID and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = ProductItem.objects.get(id=product_id)
    except ProductItem.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        quantity = request.data.get('quantity')

        if not quantity:
            return Response({'error': 'Quantity is required.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = int(quantity)
        cart_item.save()

    elif request.method == 'DELETE':
        cart_item.delete()

    serializer = CartItemSerializer(cart_item)
    cart_serializer = CartSerializer(cart_item.cart)
    return Response({'cart_item': serializer.data, 'cart': cart_serializer.data})