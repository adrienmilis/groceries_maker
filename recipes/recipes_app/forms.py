from django import forms
from .models import Ingredient, IngredientQuantity, Recipe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Button

class IngredientForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('name', placeholder='Enter ingredient name', css_class='mb-4'),
                Field('unit', css_class="form-select mb-4"),
                Field('category', css_class='form-select mb-4'),
            ),
            Div(
                ButtonHolder(
                    Submit('ingredient_form', 'Submit', css_class='mt-3')
                ), 
                css_class='col text-center',
            )
        )

    name = forms.CharField(label='Ingredient name', max_length=50)
    unit = forms.ChoiceField(label='Units', choices=Ingredient.UNIT_CHOICES)
    category = forms.ChoiceField(choices=Ingredient.CATEGORY_CHOICES)

# class RecipeForm(forms.Form):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['ingredient_ids'].label = "Ingredients"
#         self.fields['cooking_time'].label = "Cooking time (minutes)"
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Fieldset(
#                 '',
#                 Div(
#                     Field('name', css_class='mb-4', placeholder='Enter recipe name'),
#                     Field('cooking_time', css_class='mb-4'),
#                     Field('ingredient_ids', label='test', css_class='mb-4 form-select'),
#                     css_class='fields-container'
#                 )
#             ),
#             ButtonHolder(
#                 Button('add-field', 'add-field', css_class='btn-primary', onclick="addField();")
#             ),
#             Div(
#                 ButtonHolder(
#                     Submit('ingredient_form', 'Submit', css_class='mt-3')
#                 ), 
#                 css_class='col text-center',
#             )
#         )

#     name = forms.CharField(max_length=100)
#     cooking_time = forms.DurationField()
#     ingredient_ids = forms.ModelChoiceField(
#         queryset=IngredientQuantity.objects.all()
#         # widget=forms.SelectMultiple # CHOOSE A GOOD WIDGET
#     )
