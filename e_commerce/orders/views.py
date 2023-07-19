from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem, OrderDetail
from base.models import User 
from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal


from rest_framework import generics
from django.db.models import Sum
from orders.models import OrderItem
from products.models import ProductItem
from products.serializers import ProductItemSerializer
from base.models import User 
from coupon_management.models import Coupon
from django.utils import timezone
from django.contrib import messages

class BestSellingItemView(generics.ListAPIView):
    serializer_class = ProductItemSerializer

    def get_queryset(self):
        queryset = ProductItem.objects.annotate(total_units_sold=Sum('orderitem__quantity'))
        best_selling_items = queryset.order_by('-total_units_sold')
        top_2_best_selling_items = best_selling_items[:2]
        return top_2_best_selling_items    
    
    
    
    
        
# products = ProductItem.objects.annotate(total_units_sold=Sum('orderitem__quantity'))
# best_selling_items = products.order_by('-total_units_sold')

# top_10_best_selling_items = best_selling_items[:10]
       
    
@api_view(['POST'])
def make_order(request):
    user = request.user
    data = request.data
    order_items = data['order_items']
    shipping_address = data['shipping_address']
    district = data['district']
    payment_method = data['payment_method']
    coupon_code = data.get('coupon_code')
    order_total_price = Decimal(data['total_price'])

    order = Order.objects.create(user=user, shipping_address=shipping_address)

    for item in order_items:
        product = get_object_or_404(ProductItem, id=item['product_id'])
        quantity = item['quantity']
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    order_detail = OrderDetail.objects.create(order=order, payment_method=payment_method, district=district)

    # Apply coupon if provided
    discount_amount = Decimal('0')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid():
                discount_amount = coupon.get_discount_amount(order_total_price)
        except Coupon.DoesNotExist:
            pass

    order_detail.total_price = order_total_price
    order_detail.discount_amount = discount_amount
    order_detail.save()

    response_data = {
        'message': 'Order placed successfully.',
        'order_id': order.id,
        'district': district,
        'discount_amount': discount_amount,
        'total_price': order_total_price,
    }
    return Response(response_data, status=status.HTTP_201_CREATED)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal


@api_view(['GET'])
def order_list(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-date')
    order_data = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        order_item_data = []
        for order_item in order_items:
            order_item_data.append({
                'product': order_item.product.name,
                'quantity': order_item.quantity,
                'price': order_item.product.price
            })
        try:
            order_detail = OrderDetail.objects.get(order=order)
            order_total_price = order_detail.total_price
            shipping_description, shipping_price = order_detail.get_available_shipping_options() or ('No shipping option available', Decimal('0'))
            order_data.append({
                'id': order.id,
                'date': order.date,
                'status': order.status,
                'shipping_address': order.shipping_address,
                'district': order_detail.district,
                'payment_method': order_detail.payment_method,
                'shipping_option': shipping_description,
                'shipping_price': shipping_price,
                'items': order_item_data,
                'total_price': order_total_price
            })
        except OrderDetail.DoesNotExist:
            pass
    return Response(order_data)


# To Insert order details into Order Write this in the Content box in Add to order details page    
# {
#     "order_items": [
#         {
#             "product_id": 1,
#             "quantity": 2
#         },
#         {
#             "product_id": 2,
#             "quantity": 1
#         }
#     ],
#     "shipping_address": "123 Main St",
#     "district": "Zamalek",
#     "payment_method": "Credit Card"
# }
# from django.shortcuts import render
# from django.db.models import Sum
# from products.models import ProductItem
# from orders.models import OrderItem



# products = ProductItem.objects.annotate(total_units_sold=Sum('orderitem__quantity'))
# best_selling_items = products.order_by('-total_units_sold')

# top_10_best_selling_items = best_selling_items[:10]
