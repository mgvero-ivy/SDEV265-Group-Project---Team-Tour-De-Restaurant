from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inventory/", views.inventory, name="inventory"),
    path(
        "inventory/add/<int:ingredient_id>/",
        views.add_ingredient_qty,
        name="add_ingredient_qty"
    ),
    path(
        "inventory/add-new-ingredient/",
        views.add_new_ingredient,
        name="add_new_ingredient"
    ),
    path("order/", views.order_page, name="order_page"),
    path(
        "order/place/",
        views.place_order,
        name="place_order"
    ),
]