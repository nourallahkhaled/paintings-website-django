from django.shortcuts import render

# Create your views here.
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from cart.models import Cart
from wishlist.models import WishList
import stripe
from base.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request, user_id):

        user = User.objects.get(id=user_id) 
        cart = Cart.objects.get(user=user.id) 
        cart_items = cart.cartitem_set.all()
        line_items = []
        for item in cart_items:
            product = stripe.Product.create(
                name=item.product.name,  
                description=item.product.description,  
            )

            # Convert the price to an integer representing the smallest currency unit
            price_in_cents = int(item.product.price * 100)

            price = stripe.Price.create(
                unit_amount=price_in_cents,  
                currency='egp',
                product=product.id,
            )

            line_items.append({
                'price': price.id,
                'quantity': item.quantity,
            })
        try:
            checkout_session = stripe.checkout.Session.create(
                  
                line_items=line_items,
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )  
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
                    body = e.json_body
                    err = body.get('error', {})
                    return Response(
                        {'error': err.get('message')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
