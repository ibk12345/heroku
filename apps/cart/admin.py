from django.contrib import admin

from apps.cart.models import ShoppingCart, CartItem

admin.site.register(ShoppingCart)
admin.site.register(CartItem)
