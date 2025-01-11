
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from core.models import Product, Vendor, Category, ProductImages, ProductReview, CartOrderItems, CartOrder, Wishlist, Address
from userauths.models import Profile
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core import serializers

from django.db.models.functions import ExtractMonth
import calendar


# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published",featured=True).order_by("-id")
    # ProductReviews = ProductReview.objects.filter(product=products[])
    print(products)
    context = {
        "products" : products,
        # "ProductReview":ProductReviews
    }
    return render(request, "core/index.html", context)

def product_list(request):
    products = Product.objects.filter(product_status="published")
    # ProductReviews = ProductReview.objects.filter(product=products[])
    print(products)
    context = {
        "products" : products,
        # "ProductReview":ProductReviews
    }
    return render(request, "core/product_list.html", context)

def category_list(request):

    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count = Count("category"))
    context = {
        "categories":categories
    }
    return render(request, "core/category_list.html", context)

def category_product_list(request, cid):
    categories = Category.objects.all()
    category = Category.objects.get(cid = cid)
    product = Product.objects.filter(product_status = "published", category = category)

    context = {
        'category': category,
        'products':product,
        "categories":categories
    }
    return render(request, "core/category_product_list.html", context)

def vendor_list(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors" : vendors,
    }

    return render(request, "core/vendor_list.html", context)

def vendor_detail(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    product = Product.objects.filter(vendor=vendor,product_status = "published" )

    context = {
        "vendor" : vendor,
        "product" : product,
    }

    return render(request, "core/vendor_detail.html", context)

def product_Detail(request,pid):
    product = Product.objects.get(pid= pid)
    #product = get_object_or_404(Product, pid = pid)
    p_image = product.p_images.all()
    vendor = product.vendor
    products = Product.objects.filter(category = product.category).exclude(pid=pid)
    #All reviews
    reviews = ProductReview.objects.filter(product = product)
    #average rating 
    avg_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

    review_form = ProductReviewForm()

    # if uset has alredy filled the form than review form page will not be visdible to them
    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "p" : product,
        "p_images":p_image,
        "vendor":vendor,
        "products":products,
        "reviews" : reviews,
        "avg_rating" : avg_rating,
        "review_form": review_form,
        "make_review": make_review,
    }

    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):  #slug = rohan rathod ! rohan-rathod  


    products = Product.objects.filter(product_status="published").order_by("-id") #or -date

    tag = None
    if tag_slug:   # parametr
        tag = get_object_or_404(Tag, slug = tag_slug) # slug = each tag we are passing
        products = products.filter(tags__in=[tag])  #filter the product who hav tag elemnt in its tags field

    context = {
        "products" : products,
        "tag": tag,
    }

    return render(request, "core/tag.html", context)

def add_review(request, pid):
    product = Product.objects.get(pk = pid)
    user = request.user

    review = ProductReview.objects.create(        #creating new review 
        user = user,
        product = product,
        review = request.POST['review'],         #form review
        rating = request.POST['rating']
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        
    }

    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))

    return JsonResponse(       #we are doing this using javascript
        {
        'bool': True,        #hidding form
        'context':context,
        'avg_review':avg_rating,
        }
    )

    #grab ahatever send in the form

def search_view(request):
    query = request.GET.get("q")   #input name

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products":products,
        "query":query,
    }

    return render(request, "core/search.html", context)

def filter_product(request):
    categories = request.GET.getlist('category[]')  # -> data send through ajax when we click on any tag to url 
    vendors = request.GET.getlist('vendor[]')   # -> url directs here we extract the data (id) filter product show it through ajax

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()   #-> distict = filtered product

    products = products.filter(price__gte = min_price)
    products = products.filter(price__lte = max_price)

    if (len(categories) > 0 ):
        products = products.filter(category__id__in = categories).distinct()   #field lookup -> category__name__id__category__ (selecting multiple obtions)  __in -> cheking  if id exits in category
    if (len(vendors) > 0 ):
        products = products.filter(vendor__id__in = vendors).distinct()   #field lookup -> category__name__id__category__ (selecting multiple obtions)  __in -> cheking  if id exits in category

    # context = {
    #     "products" : products,
    # }

    data = render_to_string("core/async/prduct-list.html", {"products": products})
    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            request.session['cart_data_obj'].update(cart_product)
    else:
        request.session['cart_data_obj'] = cart_product

    
    totalsum = sum(
    float(item['price']) * float(item['qty']) 
    for item in request.session['cart_data_obj'].values()
    )
    total = sum(
     float(item['qty']) 
    for item in request.session['cart_data_obj'].values()
    )
    request.session['cart_total_price'] = int(totalsum)
    request.session['cart_total_products'] = int(total)


    return JsonResponse({'data': request.session['cart_data_obj'],'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products']})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for key, value in request.session['cart_data_obj'].items():
            cart_total_amount += int(value['qty']) * float(value['price'])
        return render(request, "core/cart.html", {'data': request.session['cart_data_obj'],'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products'],'cart_total_ammount':cart_total_amount})  
    else:
        messages.warning(request, "Your Cart is Empty")
        return redirect( "core:index")


def delete_from_cart(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for key, value in request.session['cart_data_obj'].items():
            cart_total_amount += int(value['qty']) * float(value['price'])
    
    
    
    totalsum = sum(
    float(item['price']) * float(item['qty']) 
    for item in request.session['cart_data_obj'].values()
    )
    total = sum(
     float(item['qty']) 
    for item in request.session['cart_data_obj'].values()
    )
    request.session['cart_total_price'] = int(totalsum)
    request.session['cart_total_products'] = int(total)

    context = render_to_string("core/async/cart-list.html", {'data': request.session['cart_data_obj'],'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products']})

    return JsonResponse({"data":context, 'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products']})
    
    # context is getting sended as data -> data contains html code used by cart-list id -> data contains data totalsum total getting used in cart-list html code
    # cart-list.html is only able to acces sended data not session data i think its becouse of js
    # in html reqest.ses.cart total prdo or .. is just an initial price when you make change like delete then total sum class name value in js is what actua;;y make changes


@csrf_exempt
def update_from_cart(request):
    if request.method == "POST":
        products = json.loads(request.POST.get("products", "{}"))
        
        print(products)
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            for product_id, qty in products.items():
                if product_id in cart_data:
                    cart_data[product_id]["qty"] = int(qty)    
                
                cart_data.update(cart_data)
                    
            request.session['cart_data_obj'] = cart_data

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for key, value in request.session['cart_data_obj'].items():
                cart_total_amount += int(value['qty']) * float(value['price'])
        
        
        
        totalsum = sum(
        float(item['price']) * float(item['qty']) 
        for item in request.session['cart_data_obj'].values()
        )
        total = sum(
        float(item['qty']) 
        for item in request.session['cart_data_obj'].values()
        )
        request.session['cart_total_price'] = int(totalsum)
        request.session['cart_total_products'] = int(total)

        context = render_to_string("core/async/cart-list.html", {'data': request.session['cart_data_obj'],'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products']},)

        return JsonResponse({"data":context, 'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products']})
    
def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
            for key, value in request.session['cart_data_obj'].items():
                cart_total_amount += int(value['qty']) * float(value['price'])

            order = CartOrder.objects.create(
                user = request.user,
                price = cart_total_amount
            )

            for key, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                cart_order_item = CartOrderItems.objects.create(
                    order = order,
                    invoice_no = "INVOICE_NO-" + str(order.id),
                    item = item['title'],
                    images = item['image'],
                    qty =item['qty'],
                    price = item['price'],
                    total = float(int(item['qty']) * float(item['price']))
                )
    try:
        user_address = Address.objects.get(user = request.user, status = True)
    except:
        messages.warning(request, "There are multiple default addresses only one should be actice")
        user_address = None

    return render(request, "core/checkout.html", {'data': request.session['cart_data_obj'],'totalsum':request.session['cart_total_price'], 'total': request.session['cart_total_products'],'cart_total_ammount':cart_total_amount, "user_address":user_address})  

@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)

    profile = Profile.objects.get(user = request.user)

    order = CartOrder.objects.annotate(month = ExtractMonth("order_date")).values("month").annotate(count = Count("id")).values("month", "count")
    month = []
    total_order = []

    for o in order:
        month.append(calendar.month_name[o['month']])
        total_order.append(o['count'])
    
    #two ways to grab address
    if request.method =="POST":
        address = request.POST.get("address")  #address in name of tag
        # address = request.POST["address"]
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            address = address,
            mobile = mobile,
            user = request.user,
        )

        messages.success(request, "Address Added successfully.")

        return redirect("core:dashboard")


    context = {
        "profile": profile,
        "orders_list": orders_list,
        "address": address,
        "order" : order,
        "month" : month,
        "total_order" : total_order,
    }
    return render( request, 'core/dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user = request.user, id = id)
    order_item = CartOrderItems.objects.filter(order = order)

    context ={
        "order_item":order_item
    }

    return render(request, "core/order_detail.html", context)

def make_default_address(request):
    id = str(request.GET['id'])
    Address.objects.update(status=False)
    Address.objects.filter(id = id).update(status = True)

    return JsonResponse({"boolean":True})

def add_to_wishlist(request):
    id = request.GET["id"]
    
    product = Product.objects.get(id = id)

    context = {

    }

    wishlist_count = Wishlist.objects.filter(product = product, user = request.user).count()

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(product = product, user = request.user)

        context = {
            "bool": True
        }
    return JsonResponse(context)

@login_required
def wishlist_view(request):
    try:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        
        
    except:
        wishlist_items = None


    context = {
        "w": wishlist_items,
        
    }
    return render(request, "core/wishlist.html", context)

def remove_wishlist(request):
    pid  = request.GET['id']
    wishlist = Wishlist.objects.filter(user = request.user)

    product = Wishlist.objects.get(id = pid)
    product = product.delete()
    

    context = {
        "bool" : True,
        "w" : wishlist,
    }

    j_wishlist = serializers.serialize('json', wishlist)

    data = render_to_string( "core/async/wishlist_list.html", context)

    return JsonResponse({"data":data, "wishlist":j_wishlist})



#Set-ExecutionPolicy Unrestricted -Scope Process
#venv\Scripts\activate
#Set-ExecutionPolicy Default -Scope Process