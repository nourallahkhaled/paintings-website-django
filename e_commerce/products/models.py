from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    start_date = models.DateTimeField()
    slug = models.SlugField(unique=True)
    discount_rate = models.PositiveIntegerField()
    end_date = models.DateTimeField()
    
    def __str__(self):
            return f"{self.slug} ({self.discount_rate}% off)"
            
class ProductItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.FloatField()
    promotion = models.ForeignKey(Promotion, related_name="promotion_items", on_delete=models.CASCADE, null=True) 
    category = models.ForeignKey(ProductCategory, related_name="category_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True)
    image = models.ImageField(null=True)
    details_image_one = models.ImageField(null=True)
    details_image_two = models.ImageField(null=True)
    details_image_three = models.ImageField(null=True)
    details_image_four = models.ImageField(null=True)
    send_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.name



