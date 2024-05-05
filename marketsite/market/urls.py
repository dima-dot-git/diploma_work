from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import MyLogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("about_us", views.about_us, name="about_us"),
    path("typography", views.typography, name="typography"),
    path("contact_us", views.contact_us, name="contact_us"),
    path("in_cart", views.in_cart, name="in_cart"),
    path("product/<int:prod_pk>", views.product, name="product"),
    path("add_to_cart/<int:prod_pk>", views.add_to_cart, name="add_to_cart"),
    path("del_of_cart/<int:prod_pk>", views.del_of_cart, name="del_of_cart"),
    path("categories/<int:cat_id>", views.categories, name="categories"),
    path("login", LoginView.as_view(), name="login_in_market"),
    path("logout", MyLogoutView.as_view(), name="logout_of_market"),
    path("registry_customer", views.registry_customer, name="registry_customer"),
    path("go_to_cart", views.go_to_cart, name="go_to_cart"),
    path("search", views.search, name="search"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("edit_profile/<int:profile_pk>", views.edit_profile, name="edit_profile"),
]
