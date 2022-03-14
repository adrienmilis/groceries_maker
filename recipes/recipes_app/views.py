from django.shortcuts import render
# from django.http import

# Create your views here.

def index(request):

    # template_name = 'index.html'
    return render(request, 'recipes_app/index.html')