from core.models import Product, Vendor, Category, ProductImages, ProductReview, CartOrderItems, CartOrder, Wishlist, Address
from django.db.models import Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendor = Vendor.objects.all()

    min_max_price = Product.objects.all().aggregate(Min('price'), Max('price'))
    wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product__id', flat=True) if request.user.is_authenticated else []


    try:
        wishlist = Wishlist.objects.filter(user = request.user)

    except:
          
        messages.warning(request, "You need to login first")
        wishlist = 0

    try:
        address = Address.objects.get(user = request.user)
    except:
        address = None

    return {
        'categories': categories,
        'address' : address,
        'vendors' : vendor,
        'min_max_price' : min_max_price,
        'wishlist':wishlist,
        'wishlist_product_ids':wishlist_product_ids,
    }
