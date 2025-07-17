import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import pymysql
pymysql.install_as_MySQLdb()

#database
USERNAME = "cf-python"
PASSWORD = "Pword4_user1"
HOST = "localhost"
DATABASE = "recipe_database"

#SQLAlchemy engine
engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

#initializing Base class
Base = sqlalchemy.orm.declarative_base()

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
    
    #calculate difficulty automatically
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"
        else:
            return


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
        try:
            name = input("Enter the name: ").strip()
            if len(name) > 50:
                print("Please keep your name below 50 characters.")
                continue

            cooking_time_input = input("Enter the number of minutes, as a number: ").strip()
            cooking_time = int(cooking_time_input)

            ingredients_input = input("Enter the ingredients, separated by a comma: ").strip()
            if not ingredients_input:
                print("Ingredients cannot be empty.")
                continue

            ingredients = ingredients_input.split(", ")
            ingredients_str = ", ".join(ingredients)

            recipe_entry = Recipe(
                name=name,
                cooking_time=cooking_time,
                ingredients=ingredients_str,
            )
            recipe_entry.calculate_difficulty()

            session.add(recipe_entry)
            session.commit()
            print("Recipe added!\n")

        except ValueError:
            print("Please enter the correct type.")
    print("Returning to main menu.")
    return None

# session.query(<model name>).filter(<model name>.
# <attribute/column name> == <value to compare against>)

def edit_recipe():
    view_all_recipes()

    #select recipe and what to change
    selected_id = int(input("Please type the ID of the recipe you would like to update: "))
    selected_recipe = session.query(Recipe).filter(Recipe.id == selected_id).first()
    print("What would you like to change?")
    print("Recipe?")
    print("Cooking Time?")
    print("Ingredients?\n")

    to_be_updated = input("Enter your choice: ").lower()
    if to_be_updated == "name":
            while True:
                new_value = input("\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    selected_recipe.name = new_value
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
                break

    elif to_be_updated == "cooking time":
        while True:
            try:
                new_value = int(input("\nEnter the new cooking time (in minutes): "))
                if new_value > 0:
                    selected_recipe.cooking_time = new_value
                    # Recalculate the difficulty after updating the cooking time.
                    selected_recipe.calculate_difficulty()
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
                selected_recipe.ingredients = new_value
                selected_recipe.calculate_difficulty()
                break
            else:
                print("Please enter at least one ingredient.") 
            break
    else:
        print("Invalid choice. Please choose 'name', 'cooking time', or 'ingredients'. Returning to main menu.")
        return None
    print("Recipe updated!")

#helper function & main menu choice
def view_all_recipes():
    recipe_list = session.query(Recipe).all()
    if not recipe_list:
        print("Please enter a recipe first!")
        return None
    for entry in recipe_list:
        display_recipe(entry)

#helper function
def display_recipe(entry):
    print(f"ID: {entry.id} | Name: {entry.name}")
    print(f"Ingredients: {entry.ingredients} | Cooking Time: {entry.cooking_time} | Difficulty: {entry.difficulty}\n")

def delete_recipe():
    #initialize and ask for ID
    view_all_recipes()
    print("Remember that a deleted recipe cannot be restored.")
    delete_id = input("\nEnter the ID of the recipe to delete: ")

    #make sure user wants to delete recipe
    double_check = input("Are you sure you'd like to delete it? Y/N: ")
    if double_check.lower() == "y":
        #delete recipe
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == delete_id).first()
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe has been deleted. Returning to main menu.")
        return None
    else:
        print("Recipe has not been deleted. Returning to main menu.")
        return None

def search_by_ingredients():
    #initialize and check that list exists
    recipe_list = session.query(Recipe).all()
    if not recipe_list:
        print("Please enter a recipe first!")
        return None
    
    #initialize all_ingredients and add to it more
    all_ingredients = set()
    for entry in recipe_list:
        ing_list = entry.ingredients.split(", ")
        for ing in ing_list:
            if ing not in all_ingredients:
                all_ingredients.add(ing)
    all_ingredients = sorted(list(all_ingredients))
    
    #Display numbered ingredients and ask for user input
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}: {ingredient}")
    ing_choices = input("Please enter the IDs of the ingredients you would like to search for, separated by spaces: ").split()
    if not all(ing.isnumeric() for ing in ing_choices):
        print("Please only enter numbers! Returning to main menu.")
        return None
    selected_ids = [int(ing_choice) for ing_choice in ing_choices]

    #construct search query with previous user input
    search_ingredients = [all_ingredients[index-1] for index in selected_ids]
    search_conditions = [Recipe.ingredients.ilike(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(or_(*search_conditions)).all()
    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    #Search for selected ingredients
    if search_results:
        for i, recipe in enumerate(search_results):
            print(f"Recipe #{i+1}:")
            display_recipe(recipe)
    else:
        print(f"No recipes contain {selected_ingredients_str}")

def main_menu():
    choice = ""
    while(choice.lower() != "quit"):
        print("What would you like to do?")
        print("1. Create a new recipe.")
        print("2. Search for a recipe.")
        print("3. Update an existing recipe.")
        print("4. Delete a recipe.")
        print("5. View all recipes.")
        choice = input("Type a number to make a choice, or type 'quit' to exit: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            search_by_ingredients()
        elif choice == '3':
            edit_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            view_all_recipes()
        elif choice == "quit":
            print("###############")
            print("Thank you for using the app! Have a good day.")
            print("###############")
        else:
            print("Invalid entry. Qutting app.")

main_menu()