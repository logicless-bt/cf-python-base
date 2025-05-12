import pickle

def take_recipe():
    name = input("Add the name of the recipe: ")
    cooking_time = int(input("Add the number of minutes it takes to cook, as an integer with no decimals: "))
    ingredients = input("Add ingredients, separated by a comma: ").split(", ")
    difficulty = calculate_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    print("Recipe received.")
    return recipe

def calculate_difficulty(cooking_time, ingredients):
    ingredient_number = len(ingredients)
    if cooking_time < 10 and ingredient_number < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and ingredient_number >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and ingredient_number < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredient_number >= 4:
        difficulty = "Hard"
    return difficulty

#try block for file access
try:
    user_input = input("Enter a filename to be accessed: ")
    with open(user_input, 'rb') as recipe_dictionary:
        data = pickle.load(recipe_dictionary)
except FileNotFoundError:
    print("No such file.")
    data = {"recipes_list": [], "all_ingredients": []}
except: 
    print("An error occurred.")
    data = {"recipes_list": [], "all_ingredients": []}

recipes_list, all_ingredients = data["recipes_list"], data["all_ingredients"]

#loop to ask for multiple recipes
n = int(input("How many recipes would you like to enter? "))
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

#update data
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

#save data to binary file
with open(user_input, "wb") as file:
    pickle.dump(data, file)

#notify user
print("Complete!")