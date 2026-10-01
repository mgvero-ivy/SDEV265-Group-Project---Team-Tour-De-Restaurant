from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ingredient, MenuItem, MenuItemIngredient, Order, OrderItem
from decimal import Decimal


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

def place_order(request):
    """
    Creates one order containing all menu items
    that the customer selected.
    """

    if request.method != "POST":
        return redirect("order_page")

    menu_items = MenuItem.objects.filter(available=True)

    selected_items = []

    # Find which menu items the customer selected.
    for menu_item in menu_items:
        quantity = int(
            request.POST.get(f"quantity_{menu_item.id}", 0)
        )

        if quantity > 0:
            selected_items.append((menu_item, quantity))

    # If nothing was selected, return to the ordering page.
    if not selected_items:
        return redirect("order_page")

    ingredient_totals = {}

    # Calculate the total amount of each ingredient needed
    # for the entire order.
    for menu_item, quantity in selected_items:

        requirements = MenuItemIngredient.objects.filter(
            menu_item=menu_item
        )

        for requirement in requirements:
            ingredient = requirement.ingredient

            amount_needed = (
                requirement.quantity_required * quantity
            )

            if ingredient.id not in ingredient_totals:
                ingredient_totals[ingredient.id] = {
                    "ingredient": ingredient,
                    "amount_needed": 0
                }

            ingredient_totals[ingredient.id]["amount_needed"] += amount_needed

    # Check inventory before creating the order.
    for item in ingredient_totals.values():

        ingredient = item["ingredient"]
        amount_needed = item["amount_needed"]

        if ingredient.quantity < amount_needed:
            return redirect("order_page")

    # Create one order for everything selected.
    order = Order.objects.create()

    # Create an OrderItem for each selected menu item.
    for menu_item, quantity in selected_items:

        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity
        )

    # Reduce inventory after the complete order has been checked.
    for item in ingredient_totals.values():

        ingredient = item["ingredient"]
        amount_needed = item["amount_needed"]

        ingredient.quantity -= amount_needed
        ingredient.save()

    messages.success(request, "Order placed successfully.")

    return redirect("order_page")

def add_ingredient_qty(request, ingredient_id):
    """To place an order for an ingredient"""
    if request.method == "POST":
        ingredient = Ingredient.objects.get(id=ingredient_id)
        qty_input = request.POST.get("quantity")
        if qty_input:
            amount_added = Decimal(qty_input)
            ingredient.quantity = ingredient.quantity + amount_added
            ingredient.save()

    return redirect("inventory")
