from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Product, Category



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','bio','avatar','role','fullname']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productName', 'price', 'quantity', 'category', 'image', 'description', 'location']
    
    # Optionally, add custom validations or choices for categories
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
