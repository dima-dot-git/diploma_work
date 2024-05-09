from django.urls import path
# from .views import stock
from . import views
urlpatterns = [
    path("", views.stock, name="stock")
]
