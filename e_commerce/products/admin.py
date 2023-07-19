# from django.contrib import admin
# from .models import ProductCategory, ProductItem, Promotion
# from django.db import models


# admin.site.register(ProductCategory)
# admin.site.register(Promotion)

# class ProductAdmin(admin.ModelAdmin):
#     # make the discount_price field optional in the admin dashboard
#     formfield_overrides = {
#         models.FloatField: {'required': False},
#     }

# admin.site.register(ProductItem, ProductAdmin)
from django.contrib import admin
from .models import ProductCategory, ProductItem, Promotion
from django.db import models
from .serializers import ProductItemSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from base.models import User
from django.core.mail import EmailMessage

admin.site.register(ProductCategory)
admin.site.register(Promotion)

class ProductAdmin(admin.ModelAdmin):
    model = ProductItem
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.send_notification:
            name = obj.name
            users = User.objects.all()
            email_list = [user.email for user in users]
            subject = 'New product added'
            message = render_to_string('mail.html')
            email = EmailMessage(subject, message, 'maryam.moh198@gmail.com', [], bcc=email_list, reply_to=['maryam.moh198@gmail.com'])
            email.content_subtype = 'html'
            email.send()   
    formfield_overrides = {
        models.FloatField: {'required': False},
    }

admin.site.register(ProductItem, ProductAdmin)


    



# from django.contrib import admin
# from .models import ProductCategory, ProductItem, Promotion
# from django.db import models
# from .serializers import ProductItemSerializer
# from django.core.mail import send_mail
# from django.template.loader import render_to_string 
# from base.models import User
# from django.core.mail import EmailMessage

# admin.site.register(ProductCategory)
# admin.site.register(Promotion)

# class ProductAdmin(admin.ModelAdmin):
#     model = ProductItem
#     def save_model(self, request, obj, form, change):
#         obj.save()

#         name = obj.name
#         users = User.objects.all()
#         email_list = [user.email for user in users]
#         subject = 'New product added'
#         message = render_to_string('mail.html', {'product_name':name})
#         email = EmailMessage(subject, message, 'maryam.moh198@gmail.com', [], bcc=email_list, reply_to=['maryam.moh198@gmail.com'])
#         email.content_subtype = 'html'
#         email.send()   
#     formfield_overrides = {
#         models.FloatField: {'required': False},
#     }

# admin.site.register(ProductItem, ProductAdmin)