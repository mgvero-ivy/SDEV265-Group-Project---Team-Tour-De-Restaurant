from django.shortcuts import render, redirect
from .models import Ingredient, MenuItem, MenuItemIngredient, Order, OrderItem


def index(request):
    """
    Display the main page of the restaurant application.

    This view renders the index.html template when a user visits
    the root URL of the website.
    """
    return render(request, "index.html")

def inventory(request):
    """
    Displays the current ingredient inventory.
    """
    ingredients = Ingredient.objects.all()

    return render(
        request,
        "inventory.html",
        {"ingredients": ingredients}
    )

def order_page(request):
    """
    Displays menu items that are currently available to order.
    """
    menu_items = MenuItem.objects.filter(available=True)

    return render(
        request,
        "order.html",
        {"menu_items": menu_items}
    )

def place_order(request, menu_item_id):
    """
    Creates an order for a selected menu item.

    This basic version only handles POST requests and records
    the menu item and requested quantity.
    """

    if request.method != "POST":
        return redirect("order_page")

    menu_item = MenuItem.objects.get(id=menu_item_id)

    requirements = MenuItemIngredient.objects.filter(menu_item=menu_item)

    quantity = int(request.POST.get("quantity", 1))

    # Check that enough of every required ingredient is available.
    for requirement in requirements:
        amount_needed = requirement.quantity_required * quantity

        if requirement.ingredient.quantity < amount_needed:
            return redirect("order_page")

    order = Order.objects.create()

    # Reduce the inventory for each ingredient used by the order.
    for requirement in requirements:
        ingredient = requirement.ingredient
        amount_needed = requirement.quantity_required * quantity

        ingredient.quantity -= amount_needed
        ingredient.save()    

    OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        quantity=quantity
    )

    return redirect("order_page")