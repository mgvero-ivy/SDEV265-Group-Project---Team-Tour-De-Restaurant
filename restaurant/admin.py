from django.contrib import admin

from .models import (
    Ingredient,
    MenuItem,
    MenuItemIngredient,
    Order,
    OrderItem,
)

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(MenuItemIngredient)
admin.site.register(Order)
admin.site.register(OrderItem)