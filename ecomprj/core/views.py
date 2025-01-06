from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import Product, Vendor, Category, ProductImages, ProductReview, CartOrderItems, CartOrder, wishlist, Address
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.template.loader import render_to_string

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

    totalsum = 0
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
        



#Set-ExecutionPolicy Unrestricted -Scope Process
#venv\Scripts\activate
#Set-ExecutionPolicy Default -Scope Process