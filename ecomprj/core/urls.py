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
    
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),


]


