from django.urls import path
from .views import StripeCheckoutView


urlpatterns = [
    path('create-checkout-session/<user_id>', StripeCheckoutView.as_view()),
]