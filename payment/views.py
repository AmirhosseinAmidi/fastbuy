from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress,Order,OrderItem
from django.contrib import messages
from store.models import Product, Profile
from django.contrib.auth.models import User

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.get_total()
    
    shipping_info = None
    shipping_form = None
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',{'cart_products':cart_products, 'quantities':quantities,'total':total, 'shipping_form': shipping_form,'shipping_info':shipping_user})
        
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',{'cart_products':cart_products, 'quantities':quantities,'total':total, 'shipping_form':shipping_form})



def confirm_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.POST
        request.session['user_shipping'] = user_shipping
        
        return render(request, 'payment/confirm_order.html',{'cart_products':cart_products, 'quantities':quantities,'total':total, 'shipping_info':user_shipping})

    else:
        messages.error(request, ' دسترسی به این صفحه امکان پذیر نیست! ')
        return redirect('home')



def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.session.get('user_shipping')
        
        full_name = user_shipping['shipping_full_name']
        email = user_shipping['shipping_email']
        full_address = f"{user_shipping['shipping_country']} - {user_shipping['shipping_city']} - {user_shipping['shipping_state']} - {user_shipping['shipping_address']} - \n منطقه : {user_shipping['shipping_zipcode']}"
        
        if request.user.is_authenticated:
            user = request.user
            new_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total,
            )
            new_order.save()
            
            ordr = get_object_or_404(Order, id =new_order.pk)
            for product in cart_products:
                prod = get_object_or_404(Product, id =product.id)
                
                if product.is_sale:
                    price = product.sale_price            
                else:    
                    price = product.price            

                for k,v in quantities.items():
                    if int(k) == prod.id:
                        new_item = OrderItem(
                            order=ordr,
                            product=prod,
                            quantity=v,
                            price=price,
                            user = user
                        )
                        new_item.save()
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
                    
            current_user = Profile.objects.filter(user__id = request.user.id)
            current_user.update(old_cart='')
                        
            messages.success(request, ' سفارش شما ثبت شد! ')
            return redirect('home')
        else:
            new_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total,
            )
            new_order.save()
            
            ordr = get_object_or_404(Order, id =new_order.pk)
            for product in cart_products:
                prod = get_object_or_404(Product, id =product.id)
                
                if product.is_sale:
                    price = product.sale_price            
                else:    
                    price = product.price            

                for k,v in quantities.items():
                    if int(k) == prod.id:
                        new_item = OrderItem(
                            order=ordr,
                            product=prod,
                            quantity=v,
                            price=price,
                        )
                        new_item.save()
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
                        
            new_order.save()
            messages.success(request, ' سفارش شما ثبت شد! ')
            return redirect('home')
        
        
    else:
        messages.error(request, ' دسترسی به این صفحه امکان پذیر نیست! ')
        return redirect('home')
