from django import forms
from .models import  ShippingAddress
from django.core.validators import RegexValidator



class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label='نام و نام خانوادگی :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'نام و نام خانوادگی خود را وارد کنید'}),
        required=True)
    
    shipping_phone = forms.CharField(
        label='شماره تلفن :',
        validators=[RegexValidator(regex=r'^\d+$', message='شماره تلفن نامعتبر می باشد.')], 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'شماره تلفن خود را وارد کنید'}),
        required=True)
    
    shipping_email = forms.EmailField(
        label='ایمیل :', 
        error_messages={'invalid':'ایمیل نامعتبر می باشد.'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'ایمیل خود را وارد کنید'}),
        required=True)
    
    shipping_address = forms.CharField(
        label='آدرس محل سکونت :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'لطفا آدرس خود را وارد کنید'}),
        required=True)
    
    shipping_city = forms.CharField(
        label='استان :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'لطفا استان خود را وارد کنید'}),
        required=True)
    
    shipping_state = forms.CharField(
        label='منطقه :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'لطفا منطقه خود را وارد کنید'}),
        required=False)
    
    shipping_zipcode = forms.CharField(
        label='کد پستی :',
        max_length=15,
        validators=[RegexValidator(regex=r'^\d+$', message='کد پستی باید فقط شامل عدد باشد.')], 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'لطفا کد پستی خود را وارد کنید','maxlength': '20'}),
        required=True)
    
    shipping_country = forms.CharField(
        label='کشور :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'لطفا کشور خود را وارد کنید'}),
        required=True)

    class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name',
                  'shipping_phone',
                  'shipping_email',
                  'shipping_address',
                  'shipping_state',
                  'shipping_city',
                  'shipping_country',
                  'shipping_zipcode',)
        
        exclude = ('user',)
