from django.shortcuts import render
from django.http import HttpResponse

from .forms import IngredientForm

def index(request):


    if request.method == 'POST':
        form = IngredientForm(request.POST)
        
        if (form.is_valid()):
            print(form.cleaned_data)
            return HttpResponse('thanks bruv')

    else:
        form = IngredientForm()

    return render(request, 'recipes_app/index.html', {'form': form})