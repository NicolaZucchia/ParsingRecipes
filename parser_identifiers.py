import spacy

nlp = spacy.load("en_core_web_sm")

# Try to spot ingredients by quantity or measures that usually get along with
def is_ingredient(line):
    ingredient_indicators = ["cup", "teaspoon", "tablespoon", "ounce", "pound", "slice", "gram", "pinch", "dash", "liter", "ml", "spoonful"]
    return any(indicator in line for indicator in ingredient_indicators)

def is_step(line):
    # Keywords that typically indicate a cooking step
    step_indicators = ["preheat", "stir", "mix", "fold", "add", "combine", "whisk", "chop", "slice", "dice", "bake", "fry", "grill", "roast", "boil"]
    return any(indicator in line for indicator in step_indicators)

def load_and_process_recipe(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    doc = nlp(text)
    
    ingredients = []
    steps = []
    other = []

    for sent in doc.sents:
        line = sent.text.strip().lower()  # Process the text in lowercase to simplify matching
        if is_ingredient(line):
            ingredients.append(sent.text.strip())
        elif is_step(line):
            steps.append(sent.text.strip())
        else:
            other.append(sent.text.strip())  # Lines that don't match ingredients or steps criteria

    return ingredients, steps, other

file_path = 'bordelaise_sauce.txt'  # Update this to the path of your recipe file
ingredients, steps, other = load_and_process_recipe(file_path)

print("Ingredients:")
for ingredient in ingredients:
    print(ingredient)
print("\nCooking Steps:")
for step in steps:
    print(step)
if other:
    print("\nOther Information:")
    for info in other:
        print(info)
