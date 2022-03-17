/*
    THE GOAL is to create an additional ingredient field

    - create the label
    - create the select and options
    - create the qty input
    - append to the div

    Besides, we must also implement some kind of input validation
    
    - check that all mandatory fields are filled
    - validate the data put in those fields
*/

let count = 3;
function addField() {
    ++count;

    // label element
    label = document.createElement('label');
    label.setAttribute('for', `recipe_ingredient_${count}`);
    label.innerText = `Ingredient ${count} - Quantity`;

    // select element
    old_select = document.getElementById('recipe_ingredient_1');
    new_select = document.createElement('select');
    new_select.innerHTML = old_select.innerHTML;
    new_select.setAttribute('name', `recipe_ingredients`);
    new_select.setAttribute('id', `recipe_ingredient_${count}`);
    new_select.setAttribute('class', "select_ingredient");

    // input quantity
    input_qty = document.createElement('input');
    input_qty.setAttribute('type', 'number');
    input_qty.setAttribute('id', `ingredient_quantity_${count}`);
    input_qty.setAttribute('name', `ingredients_quantity`);
    input_qty.setAttribute('max', '10000');

    // br
    br_1 = document.createElement('br');
    br_2 = document.createElement('br');

    // add label and select to the recipe_ingredients div
    ingredient_fields = document.querySelector('.recipe_ingredients');
    ingredient_fields.appendChild(label);
    ingredient_fields.appendChild(br_1);
    ingredient_fields.appendChild(new_select);
    ingredient_fields.appendChild(input_qty);
    ingredient_fields.appendChild(br_2);
}

/*
    FORM VALIDATION
*/

submit = document.getElementById('submit_recipe');
submit.addEventListener('click', validateForm);

function validateForm(e) {

    // create warning
    warning = document.getElementById('ingredients_warning');
    if (warning)
        warning.parentNode.removeChild(warning);
    div = document.querySelector('.recipe_ingredients');
    warning = document.createElement('p');
    warning.setAttribute('id', 'ingredients_warning');
    warning.style.cssText = 'color: red;'
    
    // an ingredient is only there once
    selects = [...document.querySelectorAll('.select_ingredient')].map(arg => arg.value);

    set_selects = new Set(selects);
    if (selects.length != set_selects.size) {
        warning.innerText = 'A ingredient can only be present once';
        e.preventDefault();
        div.appendChild(warning);
    }

}