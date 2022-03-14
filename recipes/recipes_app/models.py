from django.db import models

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

    TYPE_CHOICES = [
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
        (UNITS, 'u'),
    ]

    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=100)
    cooking_time = models.DurationField()
    ingredient_ids = models.ManyToManyField(Ingredient, through='IngredientQuantity')

    def __str__(self):
        return self.name

class IngredientQuantity(models.Model):

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        unique_together = [ ['recipe_id'], ['ingredient_id'] ]