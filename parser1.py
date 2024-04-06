import spacy
from collections import defaultdict
import re

# Load the model
nlp = spacy.load("en_core_web_md")

def parse_recipe_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    doc = nlp(text)

    # Initialize containers for ingredients and steps
    ingredients = set()
    steps = set()

    # Define a function to normalize text for comparison
    def normalize(text):
        return re.sub(r'\s+', ' ', text.strip().lower())

    # Use dependency parsing to find ingredients and steps
    for sent in doc.sents:
        roots = [token for token in sent if token.head == token]
        for root in roots:
            # Assuming steps are usually led by verbs
            if root.pos_ == "VERB":
                steps.add(normalize(sent.text))

            # Assuming ingredients might be linked to quantities or units directly
            for child in root.children:
                if child.ent_type_ in ["QUANTITY", "CARDINAL"] or child.lower_ in ["cup", "tablespoon", "teaspoon"]:
                    ingredients.add(normalize(sent.text))
                    break

    return list(ingredients), list(steps)

# Path to your recipe text file
file_path = 'sample_recipes/pancakes.txt'

# Example usage
ingredients, steps = parse_recipe_from_file(file_path)

print("Ingredients:\n", "\n".join(ingredients))
print("\nCooking Steps:\n", "\n".join(steps))
