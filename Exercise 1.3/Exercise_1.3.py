recipes_list = []
ingredients_list =[]

def take_recipe():
    name = input("Add the name of the recipe: ")
    cooking_time = int(input("Add the number of minutes it takes to cook, as an integer with no decimals: "))
    ingredients = input("Add ingredients, separated by a comma: ").split(", ")
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    print("Recipe received.")
    return recipe

def assign_difficulty(recipe):
    cooking_time = recipe["cooking_time"]
    ingredient_number = len(recipe["ingredients"])
    difficulty = None
    if cooking_time < 10 and ingredient_number < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and ingredient_number >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and ingredient_number < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredient_number >= 4:
        difficulty = "Hard"
    return difficulty

def print_recipe(recipe):
    difficulty = assign_difficulty(recipe)
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty level: " + difficulty)
    print("##########################")

n = int(input("How many recipes would you like to enter? Type a number: "))
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    print_recipe(recipe)
ingredients_list.sort()
print("Ingredients Available in All Recipes: ")
for ingredient in ingredients_list:
    print(ingredient)