from django.db import models

# Create your models here.

from base.models import User
from products.models import ProductItem
# Create your models here.
    
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

    def str(self):
        return f"{self.product.name} ({self.quantity}) in Cart for {self.user.username}"    
    
# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.product.name} added to wishlist by  {self.user.username}"