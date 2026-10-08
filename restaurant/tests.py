from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
from decimal import Decimal

from django.test import TestCase

from .models import (
    Customer,
    Ingredient,
    MenuItem,
    MenuItemIngredient,
    Order,
    OrderItem,
)


class IngredientTests(TestCase):

    def test_ingredient_can_be_created(self):
        ingredient = Ingredient.objects.create(
            name="Ground Beef",
            quantity=Decimal("10.00"),
            unit="lb",
            low_alert=Decimal("2.00"),
        )

        self.assertEqual(ingredient.name, "Ground Beef")
        self.assertEqual(ingredient.quantity, Decimal("10.00"))
        self.assertEqual(ingredient.unit, "lb")
        self.assertEqual(ingredient.low_alert, Decimal("2.00"))

    def test_ingredient_string_representation(self):
        ingredient = Ingredient.objects.create(
            name="Cheddar Cheese",
            quantity=Decimal("5.00"),
            unit="lb",
            low_alert=Decimal("1.00"),
        )

        self.assertEqual(str(ingredient), "Cheddar Cheese")


class MenuItemTests(TestCase):

    def test_menu_item_can_be_created(self):
        menu_item = MenuItem.objects.create(
            name="Cheeseburger",
            description="Beef burger with cheddar cheese",
            available=True,
            price=Decimal("12.99"),
        )

        self.assertEqual(menu_item.name, "Cheeseburger")
        self.assertTrue(menu_item.available)
        self.assertEqual(menu_item.price, Decimal("12.99"))

    def test_menu_item_is_available_by_default(self):
        menu_item = MenuItem.objects.create(
            name="French Fries"
        )

        self.assertTrue(menu_item.available)

    def test_menu_item_string_representation(self):
        menu_item = MenuItem.objects.create(
            name="Cheeseburger"
        )

        self.assertEqual(str(menu_item), "Cheeseburger")


class MenuItemIngredientTests(TestCase):

    def test_menu_item_ingredient_relationship(self):
        ingredient = Ingredient.objects.create(
            name="Ground Beef",
            quantity=Decimal("10.00"),
            unit="lb",
            low_alert=Decimal("2.00"),
        )

        menu_item = MenuItem.objects.create(
            name="Cheeseburger"
        )

        relationship = MenuItemIngredient.objects.create(
            menu_item=menu_item,
            ingredient=ingredient,
            quantity_required=Decimal("0.25"),
        )

        self.assertEqual(relationship.menu_item, menu_item)
        self.assertEqual(relationship.ingredient, ingredient)
        self.assertEqual(
            relationship.quantity_required,
            Decimal("0.25")
        )

    def test_menu_item_ingredient_string_representation(self):
        ingredient = Ingredient.objects.create(
            name="Ground Beef",
            quantity=Decimal("10.00"),
            unit="lb",
            low_alert=Decimal("2.00"),
        )

        menu_item = MenuItem.objects.create(
            name="Cheeseburger"
        )

        relationship = MenuItemIngredient.objects.create(
            menu_item=menu_item,
            ingredient=ingredient,
            quantity_required=Decimal("0.25"),
        )

        self.assertEqual(
            str(relationship),
            "Cheeseburger - Ground Beef"
        )


class OrderTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_customer"
        )
        self.customer = Customer.objects.create(user=user)

    def test_order_is_created_as_incomplete(self):
        order = Order.objects.create(customer=self.customer)

        self.assertFalse(order.completed)

    def test_order_string_representation(self):
        order = Order.objects.create(customer=self.customer)

        self.assertEqual(
            str(order),
            f"Order {order.id}"
        )


class OrderItemTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_customer"
        )
        self.customer = Customer.objects.create(user=user)

    def test_order_item_can_be_created(self):
        order = Order.objects.create(customer=self.customer)

        menu_item = MenuItem.objects.create(
            name="Cheeseburger",
            price=Decimal("12.99"),
        )

        order_item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=2,
        )

        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.menu_item, menu_item)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item_default_quantity_is_one(self):
        order = Order.objects.create(customer=self.customer)

        menu_item = MenuItem.objects.create(
            name="French Fries"
        )

        order_item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
        )

        self.assertEqual(order_item.quantity, 1)

    def test_order_item_string_representation(self):
        order = Order.objects.create(customer=self.customer)

        menu_item = MenuItem.objects.create(
            name="Cheeseburger"
        )

        order_item = OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=2,
        )

        self.assertEqual(
            str(order_item),
            "2 x Cheeseburger"
        )
