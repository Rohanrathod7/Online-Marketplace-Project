from core.models import Product, Vendor, Category, ProductImages, ProductReview, CartOrderItems, CartOrder, wishlist, Address
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    vendor = Vendor.objects.all()

    min_max_price = Product.objects.all().aggregate(Min('price'), Max('price'))
    try:
        address = Address.objects.get(user = request.user)
    except:
        address = None

    return {
        'categories': categories,
        'address' : address,
        'vendors' : vendor,
        'min_max_price' : min_max_price
    }
