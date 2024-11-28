from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
class User(AbstractUser):
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'
    ROLE_CHOICES = [(CUSTOMER, 'Customer'),
                    (SUPPLIER, 'Supplier')]
    
    fullname = models.CharField(max_length = 100)
    email = models.EmailField(null = False, unique = True)
    bio = models.TextField(null = True, blank = True )
    avatar =models.ImageField(null = True, default= 'avatar.svg', blank = True,upload_to='avatar_img/' )
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = CUSTOMER)
    #these are to setup permission s 
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)
    
class Category(models.Model):
    categoryName = models.CharField(max_length = 50 , unique = True)
    image = models.ImageField(null = True, upload_to='catagory_img/')

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., $99999999.99
    quantity = models.CharField(max_length = 10, null= False , blank = False)  # Track available stock
    category = models.ForeignKey(Category, on_delete  = models.SET_NULL, null = True)
    productName = models.CharField(max_length = 100, null = False)
    image = models.ImageField(null = True, upload_to='products_img/')
    description = models.CharField(max_length = 500, null = True )
    location  = models.CharField(max_length = 200 , null = True) 
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'supplier'})


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)  # Number of items in the cart
    
    class Meta:
        unique_together = ['product', 'user']




