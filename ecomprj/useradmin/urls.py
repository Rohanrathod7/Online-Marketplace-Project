from django.urls import path
from . import views

app_name = 'useradmin'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/edit_product/<pid>/", views.edit_product, name="edit_product"),
    path("dashboard/delete_product/<pid>/", views.delete_product, name="delete_product"),
    path("dashboard/order_detail/<id>", views.order_detail, name="order_detail"),

    path("dashboard/order_status/<id>", views.order_status, name="order_status"),
    path("dashboard/profile_settings", views.setting, name="settings")

    
]
