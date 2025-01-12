
from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, CartOrderItems, CartOrder, Address
from django.db.models import Sum
from userauths.models import User, Profile
from useradmin.forms import AddProduct
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import datetime

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price = Sum("price"))

    total_order_count =  CartOrder.objects.all()

    all_products = Product.objects.all().order_by("-id")

    all_categories = Category.objects.all()

    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all()

    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(order_date__month = this_month).aggregate(price=Sum("price"))


    if request.method == 'POST':

        form = AddProduct(request.POST, request.FILES)
        print("form submited")
        if form.is_valid():
            print("form is valid")
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            print("form saved")
            return redirect ("useradmin:dashboard")
        else:
            print("form is not valid")
            print("Form Errors:", form.errors)
    else:
        form = AddProduct()
        

    context = {
        'revenue':revenue,
        'total_order_count':total_order_count,
        'all_products':all_products,
        'all_categories':all_categories,
        'new_customers':new_customers,
        'latest_orders':latest_orders,
        'monthly_revenue':monthly_revenue,
        "form": form,
    }

    

    return render(request, "useradmin/dashboard.html", context)

    

def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect ("useradmin:edit_product", product.pid)
    else:
        form = AddProduct(instance=product)

    context = {
        "form": form,
        "product": product,
    }

    return render(request, "useradmin/edit_product.html", context)


def delete_product(request, pid):
    product = Product.objects.get(pid = pid)
    product.delete()

    return redirect ("useradmin:dashboard")

def order_detail(request, id):
    order = CartOrder.objects.get(id=id)
    user = User.objects.get(id=order.user.id)
    order_detail = CartOrderItems.objects.filter(order=order)
    profile = Profile.objects.get(user=user)
    adrs = Address.objects.get(user=user, status = True)


    return render(request, "useradmin/order_detail.html", {"order": order, "order_detail": order_detail,"profile":profile, "adrs":adrs})

@csrf_exempt
def order_status(request, id):
    order = CartOrder.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST.get("status")
        print(status)
        order.product_status = status
        order.save()
        messages.success(request, f"Order status updated")
    

    return redirect("useradmin:order_detail", order.id) 