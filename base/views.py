from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404,render,redirect
from django.views.generic import ListView,TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm,ProductUploadForm
from django.contrib.auth import login
from .models import Product,Category
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Your custom login template
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

class RegisterView(View):
    template_name = 'register.html'  # Your custom register template
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            return redirect('home')  # Redirect to home page after successful registration
        return render(request, self.template_name, {'form': form})

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add categories to the context
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        if category_id:
            # If a category is selected, filter products by that category
            return Product.objects.filter(category_id=category_id)
        # If no category is selected, return all products
        return Product.objects.all()
class ProductsView(ListView):
    model = Product
    template_name = 'products.html'  # Your template for the products page
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all categories to the context
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        # Get the category from the query parameter (if provided)
        category_id = self.request.GET.get('category', None)
        
        # If a category is selected, filter the products by that category
        if category_id:
            return Product.objects.filter(category_id=category_id)
        
        # If no category is selected, return all products
        return Product.objects.all()
class AboutView(TemplateView):
    template_name = 'about.html' 
class ProductUploadView(CreateView):
    model = Product
    form_class = ProductUploadForm
    template_name = 'upload_product.html'
    success_url = reverse_lazy('home')  # Redirect after successful upload

    def form_valid(self, form):
        # Ensure only users with the 'supplier' role can upload
        if self.request.user.role != 'supplier':
            return HttpResponseForbidden("You are not authorized to upload products.")
        
        # Set the current user as the supplier of the product
        form.instance.supplier = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Ensure that the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to add items to your cart.")

        # Get the product by ID
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the user's cart
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)

        if not created:
            # If the product is already in the cart, increase the quantity
            cart_item.quantity += 1
        cart_item.save()

        # Redirect to the home page or any other page (you can customize this)
        return redirect('home')
# Create your views here.

class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the cart items for the current user
        cart_items = Cart.objects.filter(user=self.request.user)

        # Calculate total price for all items in the cart
        total_price = sum([item.product.price * item.quantity for item in cart_items])

        # Attach total price for each item directly to the cart item
        for item in cart_items:
            item.total_price = item.product.price * item.quantity

        # Adding cart items and total price to context
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        
        return context

    def post(self, request, *args, **kwargs):
        # Get the product ID from the request to remove from the cart
        product_id = request.POST.get('product_id')
        
        if product_id:
            # Remove the product from the user's cart
            Cart.objects.filter(user=request.user, product_id=product_id).delete()
        
        return redirect('cart')  # Redirect back to the cart page
    




#IMP to check wheather cart has items
