
from django.urls import path
#from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

#router = DefaultRouter()

urlpatterns = [
    path('', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'), 
    path('home/', HomeView.as_view(), name = 'home'),
    path('products/', ProductsView.as_view(), name='products'),
      path('cart/', CartView.as_view(), name='cart'),
    path('about/', AboutView.as_view(), name='about'),
    path('home/upload/', ProductUploadView.as_view(), name='product_upload'),
    path('home/add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    
    #path('products/',views.ProductView.as_view(), name = 'prods'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)