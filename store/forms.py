from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, SetPasswordForm, PasswordChangeForm
from django import forms
from .models import Profile

class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label='تلفن :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'شماره تلفن همراه:'}),
        required=True
    )
    address1 = forms.CharField(
        label='آدرس اول :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'آدرس محل سکونت'}),
        required=True)
    address2 = forms.CharField(
        label='آدرس دوم :', 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'آدرس دوم'}),
        required=False)
    # city = forms.CharField(
    #     label='استان:', 
    #     widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'استان :'}),
    #     required=False)
    # state = forms.CharField(
    #     label='منطقه:', 
    #     widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'منطقه :'}),
    #     required=False)
    # zip_code = forms.CharField(
    #     label='کد پستی:', 
    #     widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'کد پستی :'}),
    #     required=False)
    # country = forms.CharField(
    #     label='کشور:', 
    #     widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'کشور :'}),
    #     required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1','address2')


class UpdatePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder': ' رمز عبور فعلی را وارد کنید'}),
        error_messages={'required': 'لطفاً رمز عبور فعلی را وارد کنید.'}
    )
    new_password1 = forms.CharField(
        label='رمز عبور جدید', 
        widget=forms.PasswordInput(attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder': 'رمز عبور جدید را وارد کنید'
                }),
        error_messages={'required': 'لطفاً رمز عبور جدید را وارد کنید.'} 
        )
    
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید:', 
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder': 'رمز عبور جدید را مجدد وارد کنید'
                }),
        error_messages={'required': 'لطفاً رمز عبور جدید را دوباره وارد کنید.'} 
        )
    
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')
        
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = ' form-control'



class UpdateUserForm(UserChangeForm):
    password = None
    first_name = forms.CharField(
        label='نام:', 
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام خود را وارد کنید'}), 
        )
    
    last_name = forms.CharField(
        label='نام خانوادگی:', 
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام خانوادگی خود را وارد کنید'}), 
        )
    
    email = forms.EmailField(
        label='ایمیل:', 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'ایمیل خود را وارد کنید'}), 
        )

    username = forms.CharField(
        label='نام کاربری:', 
        max_length=30, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام کاربری خود را وارد کنید'}), 
        )
    
   
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = ' form-control'

    
    class Meta:
        model = User
        fields = ("first_name","last_name", "username", "email")



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='نام:', 
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام خود را وارد کنید'}), 
        )
    
    last_name = forms.CharField(
        label='نام حانوادگی:', 
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام خانوادگی خود را وارد کنید'}), 
        )
    
    email = forms.EmailField(
        label='ایمیل:', 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'ایمیل خود را وارد کنید'}), 
        )

    username = forms.CharField(
        label='نام کاربری:', 
        max_length=30, 
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder': 'نام کاربری خود را وارد کنید'}), 
        )
    
    password1 = forms.CharField(
        label='رمز عبور', 
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder': 'رمز عبور خود را وارد کنید'
                }), 
        )
    
    password2 = forms.CharField(
        label='تکرار رمز عبور:', 
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder': 'رمز عبور را مجدد وارد کنید'
                }), 
        )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

    
    class Meta:
        model = User
        fields = ("first_name","last_name", "username", "email", "password1", "password2")