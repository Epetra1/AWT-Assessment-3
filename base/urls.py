
from django.urls import path
#from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib.auth.views import LogoutView

#router = DefaultRouter()

urlpatterns = [
    path('', CustomLoginView.as_view(), name = 'login'),
    path('home/', HomeView.as_view(), name = 'home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'), 
    path('home/upload/', ProductUploadView.as_view(), name='product_upload'),
    
    #path('products/',views.ProductView.as_view(), name = 'prods'),

]