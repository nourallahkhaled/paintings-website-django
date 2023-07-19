from django.db import models
from django.contrib.auth.models import AbstractUser , User
from django.core.validators import EmailValidator, RegexValidator

class User(AbstractUser):
    username = models.CharField( unique=True, null=False)
    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Please enter a valid email address.'
    )
    email = models.EmailField(max_length=255, unique=True, blank=False, validators=[email_regex])
    mobile_regex = RegexValidator(
        regex=r'^(010|011|012|015)\d{8}$',
        message='Please enter a valid mobile number starting with 010, 011, 012, or 015.'
    )
    mobile = models.CharField(max_length=11, unique=True, blank=False, validators=[mobile_regex])
    password_regex = RegexValidator(
        # regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{":?><,./;\'\[\]\\=-])(?!.*\s).{8,}$',
        regex=r'^(?=.\d)(?=.[a-z])(?=.[A-Z])(?=.[!@#$%^&()_+}{":?><,./;\'\[\]\\=-])(?!.\s).{8,}$',
        message='Please enter a valid password containing at least one uppercase letter, one lowercase letter, one digit, and one special character.'
    )
    password = models.CharField(max_length=255, blank=False, validators=[password_regex])
    

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='base_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='base_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self)  :
        return self.email
    
    
    
