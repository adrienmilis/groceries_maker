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
def recipe_form_2(request):

    print(request.POST)

    form_data = QueryDict(mutable=True)
    # form_data.update({
    #     'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
    #     'name': request.POST['recipe_name'],
    #     'cooking_time': request.POST['recipe_cooking_time'],
    #     # 'ingredient_ids': request.POST.getlist('recipe_ingredients')
    #     'ingredient_ids': [1,2,3]
    # })
    form_data = request.POST({'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']})
    print(form_data['ingredient_ids'])
    recipe_form = RecipeForm(form_data)

    s = ''
    if not recipe_form.is_valid():
        return (HttpResponse(f'not valid: {recipe_form.errors}'))

    list_of_cleaned_quantities = []
    for elem in request.POST.getlist('ingredients_quantity'):

        quantity_data = QueryDict(f'quantity={elem}')
        quantity_form = DummyQuantityForm(quantity_data)
        if not quantity_form.is_valid():
            return (HttpResponse(f'not valid: {quantity_form.errors}'))
        # quantity is valid
        list_of_cleaned_quantities.append(quantity_form.cleaned_data['quantity'])


    # if we made it here, form data is valid.
    # we can generate the recipe model

# USE CREATE OR CONSTRUCTOR ??
    # new_recipe = Recipe.objects.create(
    #     name=recipe_form.cleaned_data['name'],
    #     cooking_time=recipe_form.cleaned_data['cooking_time'] #str or int ??
    # )
    for ingr in enumerate(recipe_form.cleaned_data['ingredient_ids']):
        print(ingr)
    # for index, ingr in enumerate(recipe_form.cleaned_data['ingredient_ids']):
    #     print(ingr)
    #     print(list_of_cleaned_quantities[index])
    # for index, ingr in enumerate(recipe_form.cleaned_data['ingredient_ids']):
    #     new_recipe.ingredient_ids.add(
    #         Ingredient.objects.get(pk=ingr),
    #         through_defaults={'quantity': list_of_cleaned_quantities[index]}
    #     )
    # new_recipe.save()
    return (HttpResponse(f'New recipe {new_recipe.name} successfully added to database. Ingredient ids: {new_recipe.ingredient_ids.all()}, name: {new_recipe.name}, cooking_time: {new_recipe.cooking_time}'))


def recipe_form(request):

    print(request.POST)
    print(request.POST.getlist('recipe_ingredients'))
    my_dic = {
        'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken'),
        'name': request.POST.get('recipe_name'),
        'cooking_time': request.POST.get('recipe_cooking_time'),
        'ingredient_ids': request.POST.getlist('recipe_ingredients')
    }
    recipe_form = RecipeForm(my_dic)
    if not recipe_form.is_valid():
        return HttpResponse(f'not valid: {recipe_form.errors}')

    ingredient_ids_with_qty = my_dic['ingredient_ids']
    for index, qty in enumerate(request.POST.getlist('ingredients_quantity')):
        # sanitize quantity
        quantity_form = DummyQuantityForm({'quantity': qty})
        if not quantity_form.is_valid():
            return HttpResponse(f'qty not valid: {quantity_form.errors}')
        # associate it with its ingredient id
        ingredient_ids_with_qty[index] = [ingredient_ids_with_qty[index], qty]

    # create the new recipe object
    new_recipe = Recipe.objects.create(
        name=recipe_form.cleaned_data['name'],
        cooking_time=recipe_form.cleaned_data['cooking_time'],
    )

    # add its ingredients and quantities
    # for id, qty in ingredient_ids_with_qty:
    #     print('in loop')
    #     print(Ingredient.objects.get(pk=id))
    for ingr_id, qty in ingredient_ids_with_qty:
        new_recipe.ingredient_ids.add(
            Ingredient.objects.get(pk=ingr_id),
            through_defaults={'quantity': qty}
        )
    new_recipe.save()

    return HttpResponse('okkkkk')