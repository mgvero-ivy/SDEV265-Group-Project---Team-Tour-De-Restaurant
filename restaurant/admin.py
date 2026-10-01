from django.contrib import admin

from .models import (
    Ingredient,
    MenuItem,
    MenuItemIngredient,
    Order,
    OrderItem,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(MenuItemIngredient)
admin.site.register(OrderItem)