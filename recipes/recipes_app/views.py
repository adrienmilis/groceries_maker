from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError

from .forms import IngredientForm, RecipeForm
from .models import Ingredient, Recipe


def index(request):

    if request.method == 'POST':

        # creates a new ingredient
        if ('ingredient_form' in request.POST):

            ingredient_form = IngredientForm(request.POST)
            if (ingredient_form.is_valid()):

                new_ingredient = Ingredient()
                new_ingredient.name = ingredient_form.cleaned_data['name']
                new_ingredient.unit = ingredient_form.cleaned_data['unit']
                new_ingredient.category = ingredient_form.cleaned_data['category']
                try:
                    new_ingredient.save()
                except IntegrityError as e:
                    return HttpResponse('Error: there is already an ingredient with that name')

                return HttpResponse('new ingredient {} added to database'.format(ingredient_form.cleaned_data['name']))

        # creates a new recipe
        # elif ('recipe_form' in request.POST):

        #     recipe_form = RecipeForm(request.POST)
        #     if (recipe_form.is_valid()):

        #         new_recipe = Recipe()
                

    ingredient_form = IngredientForm()
    recipe_form = RecipeForm()

    return render(request, 'recipes_app/django_index.html', {
        'ingredient_form': ingredient_form, 'recipe_form': recipe_form} )

