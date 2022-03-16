from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError

from .forms import IngredientForm
from .models import Ingredient, Recipe

import re


def ingredient_form(request):

    if request.method == 'POST':

        # creates a new ingredient
        if ('ingredient_form' in request.POST):

            ingredient_form = IngredientForm(request.POST)
            if (ingredient_form.is_valid()):

                new_ingredient = Ingredient()
                new_ingredient.name = re.sub(' +', ' ', ingredient_form.cleaned_data['name']).replace(' ', '_')
                new_ingredient.unit = ingredient_form.cleaned_data['unit']
                new_ingredient.category = ingredient_form.cleaned_data['category']
                try:
                    new_ingredient.save()
                except IntegrityError as e:
                    return HttpResponse('Error: there is already an ingredient with that name')

                return HttpResponse('new ingredient {} added to database'.format(ingredient_form.cleaned_data['name']))
                
    ingredient_form = IngredientForm()
    list_1 = []
    list_2 = []
    for elem in Ingredient.objects.all():
        print(elem.name)
        list_1.append(elem.name)
        list_2.append(to_user_friendly_names(elem.name))
    list_of_ingredients = list(zip(list_1, list_2))

    return render(request, 'recipes_app/django_index.html', {
        'ingredient_form': ingredient_form,
        'ingredients': list_of_ingredients,
        })

def to_user_friendly_names(name):

    new_name = name[0].upper() + name[1:]
    new_name = new_name.replace('_', ' ')
    return new_name

def recipe_form(request):

    pass