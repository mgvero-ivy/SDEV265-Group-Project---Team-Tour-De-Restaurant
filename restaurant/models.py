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