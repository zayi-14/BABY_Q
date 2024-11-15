from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, otp=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
            otp=otp,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom user model
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # For OTP verification

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)  # New field to block users

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin  


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='products/')  # Requires Pillow for image handling
    age_upto = models.IntegerField(help_text="Age up to (in years) the product is suitable for")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.product_name


class Shortlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shortlisted_by')

    class Meta:
        unique_together = ('user', 'product')  # Each user can shortlist a product only once

    def __str__(self):
        return f"{self.user_id} - {self.product.product_name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.product.product_name} ({self.quantity})"



from .models import User, Product
from decimal import Decimal

from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField(default= 'temperary address')  # Delivery address
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} pcs"



