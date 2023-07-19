from django.db import models
from base.models import User
from products.models import ProductItem
from decimal import Decimal

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ), default='PENDING')
    shipping_address = models.CharField(max_length=200)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def _str_(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.product.price

class OrderDetail(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    payment_method = models.CharField(max_length=20, choices=(
        ('VISA', 'Visa'),
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
    ))
    DISTRICT_CHOICES = (
        ('Hadayek El Qobba', 'Hadayek El Qobba'),
        ('Zamalek', 'Zamalek'),
        ('The 5th Settlement', 'The 5th Settlement'),
        ('Masr El Gedida', 'Masr El Gedida'),
        ('Nasr City', 'Nasr City'),
        ('6th of October City', '6th of October City'),
        ('Al Haram', 'Al Haram'),
    )
    district = models.CharField(max_length=80, choices=DISTRICT_CHOICES, default='Hadayek El Qobba')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),null=True)
    first_name = models.CharField(max_length=50 , null=True)  # Add FirstName field
    phone_number = models.CharField(max_length=20 , null=True)  # Add PhoneNumber field

    def _str_(self):
        return f"Order {self.order.id} details"
   
    def get_available_shipping_options(self):
        if self.district == 'Hadayek El Qobba':
            return ('Standard Shipping (3-5 business days)', Decimal('30'))
        elif self.district == 'Zamalek':
            return ('Standard Shipping (3-5 business days)', Decimal('60'))
        elif self.district == 'The 5th Settlement':
            return ('Express Shipping (1-2 business days)', Decimal('100'))
        elif self.district == 'Masr El Gedida':
            return ('Standard Shipping (3-5 business days)', Decimal('55'))
        elif self.district == 'Nasr City':
            return ('Standard Shipping (3-5 business days)', Decimal('55'))
        elif self.district == '6th of October City':
            return ('Express Shipping (1-2 business days)', Decimal('90'))
        elif self.district == 'Al Haram':
            return ('Standard Shipping (3-5 business days)', Decimal('30'))
        else:
            return None