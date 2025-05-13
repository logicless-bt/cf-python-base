class Recipe:
    all_ingredients = set()
    #initialization
    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None
        self.update_all_ingredients()

    #name methods 
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    
    #cooking_time methods
    def get_cooking_time(self):
        return self.cooking_time
    def set_cooking_time(self, time):
        self.cooking_time = time

    #difficulty method -- the getter calculates if not present
    def calculate_difficulty(self):
        difficulty = self.difficulty
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            difficulty = "Easy"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            difficulty = "Medium"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            difficulty = "Hard"
        return difficulty
    
    def get_difficulty(self):
        if self.difficulty == None:
            self.difficulty = self.calculate_difficulty()

        return self.difficulty
    
    
    #ingredients methods
    def get_ingredients(self):
        return self.ingredients
    
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()
    
    def search_ingredients(self, ingredient):
        ingredient_lower = ingredient.lower()
        return any(ingredient_lower == ingredient.lower() for ingredient in self.ingredients)
    
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)
    
    #string representation
    def __str__(self):
        gap = "##################"
        end = "=================="
        ing_list = ', '.join(self.ingredients)
        return f"Recipe: {self.name}\n" + gap + f"\nCooking Time: {self.cooking_time} \nIngredients:{ing_list}\nDifficulty: {self.get_difficulty()}\n" + end 
    
#searching outside class, using search_ingredients() w/in class
def recipe_search(data, search_term):
    print(f"These recipes contain {search_term}\n")
    for recipe in data:
        if recipe.search_ingredients(search_term):
            print(recipe)
    
tea = Recipe("Tea", ["tea leaves", "sugar", "water"], 5)
print(tea)

coffee = Recipe("Coffee", ["coffee powder", "water", "sugar"], 5)
cake = Recipe("Cake", ["sugar", "butter", "eggs", "vanilla essence", "flour", "baking powder", "milk"], 30)
banana_smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Sugar", "Peanut Butter", "Ice Cubes"], 5)

recipes_list = [tea, coffee, cake, banana_smoothie]

recipe_search(recipes_list, "water")
recipe_search(recipes_list, "sugar")
recipe_search(recipes_list, "bananas")
