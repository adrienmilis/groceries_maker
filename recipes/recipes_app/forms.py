from django import forms
from .models import Ingredient

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field

class IngredientForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Field('name', placeholder='Enter ingredient name'),
                    css_class='mb-4'
                ),
                Div(
                    Field('unit', css_class="form-select"),
                    css_class='mb-4',
                ),
                Div(
                    Field('category', css_class='form-select'),
                    css_class='mb-4'
                )
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

class RecipeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'cooking_time',
                'ingredient_ids',
            )
        )

    name = forms.CharField(max_length=100)
    cooking_time = forms.DurationField()
    ingredient_ids = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        # widget=forms.SelectMultiple # CHOOSE A GOOD WIDGET
    )