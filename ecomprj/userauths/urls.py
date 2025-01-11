from django.urls import path
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path("contectus/", views.contectus, name="contectus"),
    path("ajax_contectus/", views.ajx_contectus, name="ajx_contectus"),
    path("profile/edit/", views.profile_update, name="profile_update"),


]
