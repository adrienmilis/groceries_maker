from django import forms

class IngredientForm(forms.Form):

    name = forms.CharField(label='Ingredient name', max_length=50)
    unit = forms.CharField(label='Units', max_length=20)
    type = forms.CharField(max_length=20)