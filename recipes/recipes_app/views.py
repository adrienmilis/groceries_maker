from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.db import IntegrityError

from .forms import IngredientForm, RecipeForm, DummyQuantityForm
from .models import Ingredient, Recipe

import re


def ingredient_form(request):

    if request.method == 'POST':

        # creates a new ingredient

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
    recipe_form = RecipeForm()
    list_of_ingredients=[]
    for elem in Ingredient.objects.all():
        list_of_ingredients.append([elem.id, to_user_friendly_names(elem.name)])

    return render(request, 'recipes_app/django_index.html', {
        'ingredient_form': ingredient_form,
        'ingredients': list_of_ingredients,
        'recipe_form': recipe_form,
        })

def to_user_friendly_names(name):

    new_name = name[0].upper() + name[1:]
    new_name = new_name.replace('_', ' ')
    return new_name


# {'csrfmiddlewaretoken': ['fDi1QEU7kwFwmLfnxpob8zc7P87rhk0hA76am1504NZ7ZBSPBcLrguliph8iHGNd'],
# 'name': ['test'],
# 'cooking_time': ['test'],
# 'ingredient_ids': ['1', '2', '3']}
def recipe_form(request):

    print(request.POST)

    form_data = QueryDict(mutable=True)
    form_data.update({
        'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
        'name': request.POST['recipe_name'],
        'cooking_time': request.POST['recipe_cooking_time'],
        'ingredient_ids': request.POST['recipe_ingredients']
    })
    recipe_form = RecipeForm(form_data)

    s = ''
    if not recipe_form.is_valid():
        return (HttpResponse('not valid'))

    for elem in request.POST.getlist('ingredients_quantity'):

        quantity_data = QueryDict(f'quantity={elem}')
        quantity_form = DummyQuantityForm(quantity_data)
        if not quantity_form.is_valid():
            return (HttpResponse('not valid'))

    # if we made it here, form data is valid.
    # we can generate the recipe model

    