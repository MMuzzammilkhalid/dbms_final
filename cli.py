# Importing necessary modules. The `os` module is used to interact with the file system for listing and managing files.
# Custom modules `file_manager` and `database_operations` are used to handle file-level operations and database-specific 
# operations such as adding, editing, and deleting records.
import os
import file_manager as fm
import database_operations as db_ops

# This function displays the main menu for the Simple DBMS application. It provides options for users to create a new database, 
# open an existing one, delete a database, or exit the program. The menu is shown repeatedly until the user selects "Exit."
def main_menu():
    print("\nSimple DBMS Main Menu")
    print("1. Create a new database")
    print("2. Open an existing database")
    print("3. Delete a database")
    print("4. Exit")

# The database menu function displays additional options once a specific database is opened. 
# Users can add new records, edit existing ones, delete records, view all records, or go back to the main menu.
def database_menu(db_name):
    print(f"\nDatabase Menu - {db_name}")
    print("1. Add a record")
    print("2. Edit a record")
    print("3. Delete a record")
    print("4. View all records")
    print("5. Back to Main Menu")

# The create_database function allows users to create a new database. It prompts the user to provide a database name 
# and define its structure by specifying field names and their maximum lengths. The function validates the inputs, 
# ensures the database doesn't already exist, and uses the file_manager module to create necessary files.
def create_database():
    db_name = input("Enter the name of the new database: ").strip()
    if not db_name:
        print("Database name cannot be empty!")
        return

    if fm.database_exists(db_name):
        print(f"A database with the name '{db_name}' already exists.")
        return

    fields = {}
    while True:
        field_name = input("Enter field name (or type 'done' to finish): ").strip()
        if field_name.lower() == 'done':
            break
        if not field_name:
            print("Field name cannot be empty.")
            continue
        if field_name in fields:
            print(f"Field '{field_name}' already exists. Please enter a unique name.")
            continue

        try:
            max_length = int(input(f"Enter maximum length for field '{field_name}': "))
            if max_length <= 0:
                print("Maximum length must be a positive integer.")
                continue
            fields[field_name] = max_length
        except ValueError:
            print("Please enter a valid integer for field length.")

    if fields:
        success = fm.create_database_files(db_name, fields)
        if success:
            print(f"Database '{db_name}' created successfully with fields: {fields}")
        else:
            print(f"Failed to create database '{db_name}'.")
    else:
        print("No fields defined. Database creation aborted.")

# This function displays a list of all available databases by scanning the current directory for database files. 
# Each database is identified by a system file that ends with '_system.json'. If no databases are found, 
# the user is informed accordingly.
def display_databases():
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]
    if not databases:
        print("No databases found.")
    else:
        print("Available Databases:")
        for i, db in enumerate(databases, start=1):
            print(f"{i}. {db}")

# The open_database function allows users to interact with an existing database. 
# It displays the list of databases, lets the user select one, and then presents a database menu for further actions 
# like adding, editing, deleting, or viewing records. The function validates user inputs and performs corresponding operations 
# through the database_operations module.
def open_database():
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]

    if not databases:
        print("No databases found. Returning to the main menu.")
        return

    display_databases()
    db_name = input("Enter the name of the database to open: ").strip()

    if not fm.database_exists(db_name):
        print(f"Database '{db_name}' does not exist.")
        return

    while True:
        database_menu(db_name)
        choice = input("Select an option: ").strip()

        if choice == "1":
            db_ops.add_record(db_name)
        elif choice == "2":
            try:
                record_index = int(input("Enter the index of the record to edit: ")) - 1
                db_ops.edit_record(db_name, record_index)
            except ValueError:
                print("Invalid input. Please enter a valid integer for the record index.")
        elif choice == "3":
            try:
                record_index = int(input("Enter the index of the record to delete: ")) - 1
                db_ops.delete_record(db_name, record_index)
            except ValueError:
                print("Invalid input. Please enter a valid integer for the record index.")
        elif choice == "4":
            db_ops.view_records(db_name)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

# The delete_database function allows users to remove an existing database. It lists all databases, lets the user select one, 
# and asks for confirmation before proceeding with deletion. The deletion process is handled by the file_manager module.
def delete_database():
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]

    if not databases:
        print("No databases found. Returning to the main menu.")
        return

    display_databases()
    db_name = input("Enter the name of the database to delete: ").strip()

    if not fm.database_exists(db_name):
        print(f"Database '{db_name}' does not exist.")
        return

    confirm = input(f"Are you sure you want to delete the database '{db_name}'? (yes/no): ").strip().lower()
    if confirm == 'yes':
        fm.delete_database(db_name)
    else:
        print("Deletion canceled.")

# The run_cli function serves as the entry point for the Simple DBMS application. 
# It displays the main menu and executes the corresponding functionality based on user input. 
# The loop continues until the user selects the "Exit" option.
def run_cli():
    while True:
        main_menu()
        option = input("Select an option: ").strip()

        if option == '1':
            create_database()
        elif option == '2':
            open_database()
        elif option == '3':
            delete_database()
        elif option == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

# This condition ensures the script runs the CLI only when executed directly (not when imported as a module).
if __name__ == "__main__":
    run_cli()
