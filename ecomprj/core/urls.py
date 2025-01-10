from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    #home
    path("", views.index, name='index'),
    path("products/", views.product_list, name='product_list'),
    path("product/<pid>/", views.product_Detail, name='product_detail'),

    #category
    path("category/", views.category_list, name='category_list'),
    path("category/<cid>/", views.category_product_list, name='category_product_list1'),
    #vendor
    path("vendor/", views.vendor_list, name = "vendor_list"),
    path("vendor/<vid>/", views.vendor_detail, name = "vendor_detail"),

    #tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name  = "tags"),

    #review
    path("add_review/<int:pid>/", views.add_review, name = "add_review"),

    path("search/", views.search_view, name="search"),

    path("filter_product/", views.filter_product, name="filter_product"),
    
    #add to cart url
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),

    #cart page 
    path("cart/", views.cart_view, name="cart"),

    path("delete-from-cart/", views.delete_from_cart, name="delete-from-cart"),

    path("update_from_cart/", views.update_from_cart, name="update_from_cart"),

    path("checkout/", views.checkout_view, name="checkout"),

    path("dashboard/",views.customer_dashboard, name="dashboard"),

    path("dashboard/order/<int:id>", views.order_detail, name="order_detail"),

    path("make_default_address/", views.make_default_address, name="make_default-address")


]


