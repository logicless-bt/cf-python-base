import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()

#initializing Session
Session = sessionmaker(bind=engine)
session = Session()

#Recipe class
class Recipe(Base):
    __tablename__ = "practice_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    #used for debugging
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
    #front-facing, user-friendly representation
    def __str__(recipe):
        print(f"Recipe: {recipe[1].title()}")
        print(f"Time: {recipe[3]} mins")
        print("Ingredients: ")
        for ingredient in recipe[2].split(", "):
            print(f"- {ingredient.title()}")
        print(f"Difficulty: {recipe[4]}")
        return 

def calculate_difficulty(self, cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        self.difficulty = "Easy"
        return 
    elif cooking_time < 10 and num_ingredients >= 4:
        self.difficulty = "Medium"
        return
    elif cooking_time >= 10 and num_ingredients < 4:
        self.difficulty = "Intermediate"
        return
    elif cooking_time >= 10 and num_ingredients >= 4:
        self.difficulty = "Hard"
        return 
    
def return_ingredients_as_list(self):
    ingredient_list = []
    if not self.ingredients:
        return ingredient_list
    ingredient_list = self.ingredients.split(", ")
    return ingredient_list

#finalizing Base to create table
Base.metadata.create_all(engine)


#if database is empty:
    #  tea = Recipe(
#         name = "Tea",
#         cooking_time = 5,
#         ingredients = "Tea Leaves, Water, Sugar"
# )
#session.add(tea)
#session.commit()

#functions called by main menu
def create_recipe():
    print("\n")
    try:
        number_of_recipes = int(input("How many recipes would you like to add? "))
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

    for i in range(number_of_recipes):
        print(f"Enter recipe #{i+1}")
        print("=================")

        name = input("Enter the name: ")
        if len(name) > 50:
            print("Please keep your name below 50 characters.")
            return
        cooking_time = int(input("Enter the number of minutes, as a number: "))
        if not cooking_time.isnumeric():
            print("Please only enter numbers")
            return
        ingredients_input = input("Enter the ingredients, separated by a comma: ")
        ingredients = ingredients_input.split(", ")
        difficulty = calculate_difficulty(cooking_time, ingredients)

        ingredients_str = ", ".join(ingredients)

        try: 
            recipe_entry = Recipe(
                name = name,
                cooking_time = cooking_time,
                ingredients = ingredients_str,
                difficulty = difficulty
            )
            session.add(recipe_entry)
            session.commit()
            print("Recipe added!\n")
        except:
            print("Error occurred.")
    print("Returning to main menu.")

# session.query(<model name>).filter(<model name>.
# <attribute/column name> == <value to compare against>)

def update_recipe():
    #print easily read representations, and check to make sure they exist
    recipe_list = session.query(Recipe).all()
    if not recipe_list:
        print ("Please enter a recipe first!")
        return
    for entry in recipe_list:
        print(f"ID: {entry.id} | Name: {entry.name}")
        print(f"Ingredients: {entry.ingredients} | Cooking Time: {entry.cooking_time} | Difficulty: {entry.difficulty}\n")


    selected_id = int(input("Please type the ID of the recipe you would like to update: "))
    selected_recipe = session.query(Recipe).filter(Recipe.id == selected_id)
    print("What would you like to change?")
    print("Recipe?")
    print("Cooking Time?")
    print("Ingredients?\n")

    to_be_updated = input("Enter your choice: ").lower()
    if to_be_updated == "name":
            while True:
                new_value = input("\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    recipe_to_update.name = new_value
                    field_updated = True
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
                break

    elif to_be_updated == "cooking time":
        while True:
            try:
                new_value = int(input("\nEnter the new cooking time (in minutes): "))
                if new_value > 0:
                    recipe_to_update.cooking_time = new_value
                    # Recalculate the difficulty after updating the cooking time.
                    recipe_to_update.calculate_difficulty()
                    field_updated = True
                    break
                else:
                    print("Please enter a positive number for cooking time.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for cooking time.")
            break
                    
    elif to_be_updated == "ingredients":
        while True:
            new_value = input("\nEnter the new ingredients, separated by a comma: ").strip()
            if new_value:
                # Update the ingredients and recalculate the difficulty.
                recipe_to_update.ingredients = new_value
                recipe_to_update.calculate_difficulty()
                field_updated = True
                break
            else:
                print("Please enter at least one ingredient.") 
            break
    else:
        print("Invalid choice. Please choose 'name', 'cooking time', or 'ingredients'.")