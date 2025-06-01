from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField
from store.models import Product
from django.db.models.signals import post_save
from store.models import Customer
from django_jalali.db import models as jmodels
import jdatetime



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_phone = models.CharField(max_length=15)
    shipping_email = models.EmailField()
    shipping_address = models.CharField(max_length=250, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100,blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=15,blank=True, null=True)
    shipping_country = models.CharField(max_length=100, default='ایران')
    
    class Meta:
        verbose_name_plural = 'Shipping Address'
        
    def __str__(self):
        return f'Shipping Address From : {self.shipping_full_name}'
    
def create_shipping_user(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
        
post_save.connect(create_shipping_user, sender=User)

    

class Order(models.Model):
    STATUS_ORDER = [
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'لغو شده')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    shipping_address = models.TextField(max_length=150000)
    amount_paid = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_ORDER, default='pending')
    last_update = jmodels.jDateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status
            if old_status != self.status:
                self.last_update = jdatetime.datetime.now()
        super().save(*args, **kwargs)
    
    
    
    
    def __str__(self):
        return f'Order From : {self.id}'
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    
    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        if self.user is not None:
            return f'Order item : {str(self.product.category)} | from : {self.user}'
        else:
            return f'Order item : {str(self.product.category)} | from : {self.order.full_name}'
