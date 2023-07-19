from django.urls import path
from .views import Product_List, Product_Details
from products import views

urlpatterns = [
    path('', Product_List.as_view()),
    path('<int:id>/', Product_Details.as_view()),
    path('promotions/<int:promotion_id>/', views.get_discount_rate, name='get_discount_rate'),
]