from multiprocessing import context
from os import name
from django.shortcuts import render,redirect

from .models import Order, Product,Category, Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm,UpdatePasswordForm,UpdateUserInfo
from django.db.models import Q
import json
from cart.cart import Cart
from payment.models import ShippingAddress, Order ,OrderItem
from payment.forms import ShippingForm
from store.models import Customer



def orders_details(request, pk):
    cart_products = Cart(request).get_prods()
    quantities = Cart(request).get_quants()
    total_price = 0
    if not request.user.is_authenticated:
        messages.warning(request, 'ابتدا وارد شوید!') 
        return redirect('login')
    else:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order =pk)

        context = {
            'order':order,
            'items':items,
        }
        
        
    return render(request, 'orders_details.html', context)


def user_orders(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'ابتدا وارد شوید!') 
        return redirect('login')
    else:
        delivered_orders = Order.objects.filter(user = request.user, status = 'delivered')
        other_orders = Order.objects.filter(user = request.user).exclude(status = 'delivered')
        
        context = {
            'delivered':delivered_orders,
            'other':other_orders,
            
        }
        
        
        return render(request, 'orders.html', context)

def search(request):
    searched_query = request.GET.get('searched')
    if searched_query:
        searched = Product.objects.filter(
            Q(name__icontains=searched_query) | Q(description__icontains=searched_query) | Q(category__name__icontains=searched_query)
            )
        if not searched:
            messages.warning(request, 'چیزی مطابق سرچ شما یافت نشد!')
            return redirect('home')
        else:
            return render(request, 'search.html', {'searched':searched})
    return render(request, 'search.html', {})


# def search(request):
#     if request.method == 'POST':
#         searched = request.POST['searched']
#         searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
#         if not searched:
#             messages.warning(request, 'چیزی مطابق سرچ شما یافت نشد!')
#             return render(request, 'search.html', {})
#         else:
#             return render(request, 'search.html', {'searched':searched})
#     return render(request, 'search.html', {})


def category_summary(request):
    all_cat = Category.objects.all()
    return render(request, 'category_summary.html', {'category': all_cat})


def helloworld(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'product':all_products})

def aboutus(request):
    return render(request, 'aboutus.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            current_user = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            
            if saved_cart:
                converted_cart = json.loads(saved_cart)

                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                    
            
            messages.success(request, "با موفقیت وارد شدید!")
            return redirect('home')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است!") 
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    return redirect('home')


def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, "ثبت نام موفقیت آمیز بود!")
            return redirect('update_info')
        else:
            messages.error(request, "ثبت نام موفقیت آمیز نبود!")
            messages.error(request, "لطفا خطا ها را بررسی کنید!")
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None , instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "ویرایش اطلاعات با موفقیت انجام شد!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})

    else:
        messages.error(request, "ابتدا وارد شوید!")
        return redirect('login')

def update_info(request):
    if not request.user.is_authenticated:                      # ← __تغییر: شرط ساده‌تر__
        messages.error(request, "ابتدا وارد شوید!")
        return redirect('login')

    current_user = Profile.objects.get(user=request.user)
    shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)  # ← __تغییر: جلوگیری از خطای get__

    info_form = UpdateUserInfo(request.POST or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    if request.method == 'POST':                               # ← __تغییر: چک کردن فقط در POST__
        if info_form.is_valid() and shipping_form.is_valid():  # ← __تغییر: and به جای or برای اعتبارسنجی صحیح__
            info_form.save()
            shipping_form.save()
            messages.success(request, "اطلاعات کاربری شما ثبت شد!")
            return redirect('update_info')
        else:
            print("Info Form Errors:", info_form.errors)
            print("Shipping Form Errors:", shipping_form.errors)
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")

    return render(request, 'update_info.html', {
        'info_form': info_form,
        'shipping_form': shipping_form
    })



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
                ####################################
                # for error_list in form.errors.values():
                #     for error in error_list:
                #         messages.error(request, error)
                # return redirect('update_password')
                    
            
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.error(request, "ابتدا وارد حساب کاربری خود شوید!") 
        return redirect('login')
    return render(request, 'update_password.html', {})


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request,cat):
    cat = cat.replace('-',' ')
    try:
        category = Category.objects.get(name=cat)
        product = Product.objects.filter(category=category)
        return render(request, 'category.html', {'product':product, 'category':category})
    except:
        messages.error(request, "دسته بندی یافت نشد!")
        return redirect('home')
