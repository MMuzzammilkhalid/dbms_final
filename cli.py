import os
import file_manager as fm
import database_operations as db_ops


def main_menu():
    """Displays the main menu options."""
    print("\nSimple DBMS Main Menu")
    print("1. Create a new database")
    print("2. Open an existing database")
    print("3. Delete a database")
    print("4. Exit")


def database_menu(db_name):
    """Displays the database menu options."""
    print(f"\nDatabase Menu - {db_name}")
    print("1. Add a record")
    print("2. Edit a record")
    print("3. Delete a record")
    print("4. View all records")
    print("5. Back to Main Menu")


def create_database():
    """Creates a new database."""
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
            fields[field_name] = max_length
        except ValueError:
            print("Please enter a valid integer for field length.")

    if fields:
        success = fm.create_database_files(db_name, fields)
        if success:
            print(f"Database '{db_name}' created successfully with fields: {fields}")
        else:
            print(f"Failed to create database '{db_name}'.")


def display_databases():
    """Displays all available databases."""
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]
    if not databases:
        print("No databases found.")
    else:
        print("Available Databases:")
        for i, db in enumerate(databases, start=1):
            print(f"{i}. {db}")


def open_database():
    """Opens an existing database."""
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


def delete_database():
    """Deletes an existing database."""
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


def run_cli():
    """Runs the command-line interface for the Simple DBMS."""
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


if __name__ == "__main__":
    run_cli()
