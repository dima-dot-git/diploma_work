from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Profile, ProductInCart, Product, Category, Brand, PhotoProduct, Cart, Stock, ProductInStock,
                     Subscribe)

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(PhotoProduct)
admin.site.register(Cart)
admin.site.register(Stock)
admin.site.register(ProductInStock)
admin.site.register(ProductInCart)
admin.site.register(Profile)
admin.site.register(Subscribe)

