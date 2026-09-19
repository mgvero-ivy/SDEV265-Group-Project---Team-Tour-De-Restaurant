from django.core.validators import MinValueValidator
from django.db import models

class Ingredient(models.Model):
    """
    Represents an ingredient that the restaurant keeps in inventory.

    Each ingredient stores its current quantity, the unit used to measure
    that quantity, and a low_alert that can later be used to identify
    low inventory.
    """

    # Name of the ingredient, such as "Ground Beef" or "Cheddar Cheese".
    name = models.CharField(max_length=100)

    # Current amount of this ingredient available in inventory.
    # DecimalField is used because inventory quantities may include fractions.
    # MinValueValidator prevents users from entering a negative inventory amount.
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    # Unit used to measure this ingredient.
    # Examples: "lb", "oz", "each", "gallon", or "slice".
    unit = models.CharField(max_length=20)

    # Inventory level at which the ingredient should trigger a low stock warning.
    # Values must be 0 or higher.
    low_alert = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        """
        Controls how an Ingredient object is displayed in Django.

        Instead of showing something like "Ingredient object (1)",
        Django will display the ingredient's actual name.
        """
        return self.name


class MenuItem(models.Model):
    # Name of the menu item
    # Must be string of 100 characters or less
    name = models.CharField(max_length=100)

    # Optional description
     # Not in currently in use by the program but may be used in the future
    description = models.TextField(blank=True)

    # Determines whether customers/employees can currently order this item
    available = models.BooleanField(default=True)

    # Menu price
    # Not in currently planned for the program but may be used in the future
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class MenuItemIngredient(models.Model):
    """
    Connects a MenuItem to an Ingredient.

    This model records which ingredients are required for each menu item
    and how much of each ingredient is needed to prepare one order.

    Example:
        Cheeseburger -> Beef -> 1 patty
        Cheeseburger -> Cheddar Cheese -> 1 slice
    """

    # The menu item that uses this ingredient.
    # If the menu item is deleted, its ingredient relationships
    # will also be deleted.
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    # The ingredient required to prepare the menu item.
    # If the ingredient is deleted, the relationship is also deleted.
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )

    # Amount of this ingredient required to prepare one menu item.
    # MinValueValidator prevents negative required quantities.
    quantity_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
        
    )

    def __str__(self):
        """
        Displays a readable description of the relationship.
        """
        return f"{self.menu_item} - {self.ingredient}"


class Order(models.Model):
    """
    Represents a customer order placed in the restaurant system.

    Each order stores the date and time it was created and whether
    the order has been completed.
    """

    # Automatically records the date and time when the order is first created.
    # auto_now_add=True means this value is set once and then stays unchanged.
    created_at = models.DateTimeField(auto_now_add=True)

    # Tracks whether the order has been completed.
    # New orders start as incomplete so they can later be marked complete.
    completed = models.BooleanField(default=False)

    def __str__(self):
        """
        Displays a readable name for the order in Django.
        """
        return f"Order {self.id}"


class OrderItem(models.Model):
    """
    Represents one menu item that belongs to an order.

    Each OrderItem connects an Order to a MenuItem and stores
    how many of that menu item were ordered.

    Example:
        Order 12 -> Cheeseburger -> quantity 2
    """

    # The order that this item belongs to.
    # If the order is deleted, its OrderItem records are also deleted.
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    # The menu item that was ordered.
    # If the menu item is deleted, its related OrderItem records
    # will also be deleted.
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    # Number of this menu item included in the order.
    # MinValueValidator(1) prevents quantities of 0 or negative numbers.
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        """
        Displays the menu item and quantity in a readable format.
        """
        return f"{self.quantity} x {self.menu_item}"