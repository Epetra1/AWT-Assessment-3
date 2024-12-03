from .models import Cart

def cart_items(request):
    if request.user.is_authenticated:
        cart_items_count = Cart.objects.filter(user=request.user).count()  # Get the count of items
    else:
        cart_items_count = 0

    return {
        'cart_items_count': cart_items_count  # Make sure this is what you're passing to the template
    }
