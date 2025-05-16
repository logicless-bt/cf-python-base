import mysql.connector
conn = conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='Pword4_user1')
cursor = conn.cursor

#setting up and accessing database
cursor.execute("CREATE DATABASE IF NOT EXISTS recipe_database")
cursor.execute("USE recipe_database")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ""
    while(choice != quit):
        print("What would you like to do?")
        print("1. Create a new recipe.")
        print("2. Search for a recipe.")
        print("3. Update an existing recipe.")
        print("4. Delete a recipe.")
        choice = input("Type a number to make a choice: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            search_recipe()
        elif choice == '3':
            update_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == "quit":
            print("###############")
            print("Thank you for using the app! Have a good day.")
            print("###############")
        else:
            print("Invalid entry. Qutting app.")

def create_recipe(conn, cursor):
    print("\n")
    try:
        number_of_recipes = input("How many recipes would you like to add? ")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

    for i in range(number_of_recipes):
        print(f"Enter recipe ${i+1}")
        print("=================")

        name =  input("Enter the name: ")
        cooking_time = int(input("Enter the number of minutes, as a number: "))
        ingredients_input = input("Enter the ingredients, separated by a comma: ")
        ingredients = input(ingredients_input.split(", "))
        difficulty = calculate_difficulty(cooking_time, ingredients)

        ingredients_str = ", ".join(ingredients)

        try: 
            insert_query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, ingredients_str, cooking_time, difficulty))
            conn.commit()
            print("Recipe added!\n")
        except:
            print("Error occurred.")
    print("Returning to main menu.")

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"
    
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    if not results:
        print("Please enter a recipe first!\n")

    all_ingredients=set()
    print("Search for a Recipe")
    print("###################")

    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    for i, ingredient in enumerate(sorted(all_ingredients)):
        print(f"{i+1}.) {ingredient.title()}")
    print()
    while True:
        try:
            choice = int(input("Enter a number for the ingredient: "))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print()
                print("Please enter a number within the list range.\n")
        except ValueError:
            print()
            print("Invalid input. Please enter a number.\n")

    selected_ingredient = sorted(all_ingredients)[choice - 1]
    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s" 
    cursor.execute(search_query, ("%" + selected_ingredient + "%",))
    search_results = cursor.fetchall()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{selected_ingredient.title()}'\n")
        for recipe in search_results:
            display_recipe(recipe)

        print()
        print("...returning to main menu\n")
    else:
        print(f"No recipes found containing '{selected_ingredient.title()}'\n")
    print("\n")

def display_recipe(recipe):
    print(f"\nRecipe: {recipe.name}")
    print(f"Time: {recipe.cooking_time} mins")
    print("Ingredients: ")
    for ingredient in recipe:
        print(f"- {ingredient}")
    print(f"Difficulty: {recipe.difficulty}")

def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("Please add a recipe first!")
        return
    
    for result in results:
        ingredients_list = results[2].split(", ")
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            print()
            recipe_id = int(input("Enter the ID of the recipe to update: "))
            print()

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                break
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")
    selected_recipe = next((recipe for recipe in results if recipe[0] == recipe_id), None)
    if selected_recipe:
        print(f"Which field would you like to update for '{selected_recipe[1]}'?")
    else:
        print("Recipe not found.")
        return
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    update_field = input("Enter your choice: ").lower()
    print()

    if update_field == "cooking time":
        update_field = "cooking_time"

    if update_field not in ["name", "cooking_time", "ingredients"]:
        print("Invalid field. Please enter 'name', 'cooking_time', or 'ingredients'.")
        return
    
    if update_field == "cooking_time" or update_field == "cooking time":
        while True:
            try:
                new_value = int(input("Enter the new cooking time (in minutes): "))
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for cooking time.")
    else:
        new_value = input(f"Enter the new value for {update_field}: ")

    update_query = f"UPDATE Recipes SET {update_field} = %s WHERE id = %s"
    cursor.execute(update_query, (new_value, recipe_id))

    if update_field in ["cooking_time", "ingredients"]:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe = cursor.fetchone()
        new_difficulty = calculate_difficulty(int(updated_recipe[0]), updated_recipe[1].split(", "))

        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    conn.commit()

    print("Recipe updated.")
    print("...returning to main menu\n\n")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("There are no recipes to delete.")
        print("returning to main menu\n\n")
        return
    
    print("Please enter the ID number of the recipe to permanently remove.")

    
    print("---- Avaiable Recipes ----\n")
    for result in results:
        ingredients_list = result[2].split(", ")
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to delete: "))
            print()

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                
                cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
                recipe_name = cursor.fetchone()[0]
                confirm = input(f"Are you sure you want to delete '{recipe_name}'? (Yes/No): ").lower()
                
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print()
                    print("Deletion cancelled. Returning to main menu\n\n")
                    return
                else:
                    print()
                    print("Please answer with 'Yes' or 'No'.\n")
                
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))

    conn.commit()

    print("Recipe deleted.")
    print("Returning to main menu\n\n")

main_menu(conn, cursor)
