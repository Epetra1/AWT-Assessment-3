from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm,ProductUploadForm
from django.contrib.auth import login
from .models import Product,Category
from django.http import HttpResponseForbidden

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


# Create your views here.

