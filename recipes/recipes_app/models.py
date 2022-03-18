from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# custom CharField to ensure name is always in lowercase
class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Ingredient(models.Model):

    FRUITS_AND_VEGGIES = 'F_V'
    DAIRY = 'DA'
    FROZEN = 'FR'
    BAKERY = 'BK'
    MEAT_AND_FISH = 'M_F'
    CANNED = 'CA'
    SPICES = 'SP'
    DRY = 'DR'
    PREMADE = 'PR'
    OTHER = 'O'

    CATEGORY_CHOICES = [
        (FRUITS_AND_VEGGIES, 'Fruits and vegetables'),
        (DAIRY, 'Dairy'),
        (FROZEN, 'Frozen'),
        (BAKERY, 'Bakery'),
        (MEAT_AND_FISH, 'Meat and fish'),
        (CANNED, 'Canned'),
        (SPICES, 'Spices'),
        (DRY, 'Dry'),
        (PREMADE, 'Premade'),
        (OTHER, 'Other'),
    ]

    MILLILITERS = 'ML'
    GRAMS = 'G'
    UNITS = 'U'


    UNIT_CHOICES = [
        (MILLILITERS, 'ml'),
        (GRAMS, 'g'),
        (UNITS, 'units'),
    ]

    name = NameField(max_length=50, unique=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Recipe(models.Model):

    name = NameField(max_length=100, unique=True)
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
    ) # or integer ?
    ingredient_ids = models.ManyToManyField(Ingredient, through='IngredientQuantity')

    def __str__(self):
        return self.name

class IngredientQuantity(models.Model):

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
    )

    def __str__(self):
        return f'{self.recipe_id.name}: {self.ingredient_id.name} ({self.quantity}{self.ingredient_id.unit})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe_id', 'ingredient_id'], name='ingredient_unique_in_recipe')
        ]
