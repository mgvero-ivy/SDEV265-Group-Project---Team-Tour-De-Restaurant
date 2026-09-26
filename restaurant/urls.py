from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/add/<int:ingredient_id>/", views.add_ingredient_qty, name="add_ingredient_qty"),
    path("order/", views.order_page, name="order_page"),
    path(
        "order/<int:menu_item_id>/",
        views.place_order,
        name="place_order"
    ),
]