from django.urls import path
from .views import  make_order, order_list, BestSellingItemView

urlpatterns = [
    path('bestSelling/', BestSellingItemView.as_view()),
    path('order_details/', make_order),
    path('order_list/', order_list),
]