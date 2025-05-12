import pickle

def display_recipe(recipe):
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(f"Difficulty level: " + recipe["difficulty"])
    print("##########################")

def search_ingredients(data):
    all_ingredients = data["all_ingredients"]
    for i, ingredient in enumerate(data['all_ingredients']):
        print(f"#{i+1}. {ingredient}")
    try:
        index = int(input("Search for an ingredient by its index: "))
        ingredient_searched = all_ingredients[index-1]
    #finding recipes and counting/displaying them
        recipes_searched = [recipe for recipe in data["recipes_list"] if ingredient_searched in recipe["ingredients"]]
        print(f"Recipes found with {ingredient_searched}: ")
        for recipe in recipes_searched:
            display_recipe(recipe)
    except ValueError:
        print("Error received. Did you enter a number?")
    except IndexError:
        print("That index does not exist.")

#actual execution:
filename = input("Enter a filename to be accessed: ")
try: 
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please check for typos and check data structure.")
else: 
    search_ingredients(data)