from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User , auto_now=True)
    phone = models.CharField(max_length=25, blank=True)
    address1 = models.CharField(max_length=250, blank=True)
    address2 = models.CharField(max_length=250, blank=True)
    # city = models.CharField(max_length=25, blank=True)
    # state = models.CharField(max_length=25, blank=True)
    # zip_code = models.CharField(max_length=25, blank=True)
    # country = models.CharField(max_length=25, default='IRAN')
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)


    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default='',null=True, blank=True)
    price = models.DecimalField(default=0 , max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='upload/products/', blank=True, null=True)
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    
    
    def __str__(self):
        return self.name
 
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=250, default='', null=True, blank=True)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.name