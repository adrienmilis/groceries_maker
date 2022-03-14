from django.contrib import admin
from .models import Ingredient, Recipe, IngredientQuantity

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientQuantity)
# Register your models here.
