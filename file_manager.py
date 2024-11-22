import json
import os


def delete_database(db_name):
    """
    Deletes the specified database by removing its associated files.
    """
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

    try:
        # Remove the data file if it exists
        if os.path.exists(data_file):
            os.remove(data_file)
            print(f"Deleted data file: {data_file}")
        else:
            print(f"Data file '{data_file}' not found.")

        # Remove the system file if it exists
        if os.path.exists(system_file):
            os.remove(system_file)
            print(f"Deleted system file: {system_file}")
        else:
            print(f"System file '{system_file}' not found.")

        print(f"Database '{db_name}' has been deleted successfully.")
    except Exception as e:
        print(f"Error deleting database '{db_name}': {e}")


def create_database_files(db_name, fields):
    """
    Creates the necessary files for a new database, including data and system files.
    """
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

    try:
        with open(system_file, 'w') as f:
            json.dump(fields, f, indent=4)  # Save metadata (fields)
        with open(data_file, 'w') as f:
            json.dump([], f, indent=4)  # Initialize with an empty list of records
        print(f"Database '{db_name}' created successfully.")
        return True  # Indicate success
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error creating database files: {e}")
        return False  # Indicate failure


def load_system_file(db_name):
    """
    Loads the system file (metadata) for the specified database.
    """
    system_file = f"{db_name}_system.json"
    if not os.path.exists(system_file):
        print(f"System file for database '{db_name}' not found.")
        return None

    try:
        with open(system_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: System file for '{db_name}' is corrupted.")
        return None


def load_data_file(db_name):
    """
    Loads the data file (records) for the specified database.
    """
    data_file = f"{db_name}_data.json"
    if not os.path.exists(data_file):
        print(f"Data file for database '{db_name}' not found.")
        return []

    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Data file for '{db_name}' is corrupted.")
        return []


def save_data_file(db_name, records):
    """
    Saves the records to the data file for the specified database.
    """
    data_file = f"{db_name}_data.json"

    try:
        with open(data_file, 'w') as f:
            json.dump(records, f, indent=4)
        print(f"Records saved successfully to '{db_name}'.")
    except IOError as e:
        print(f"Error saving records to '{db_name}_data.json': {e}")


def database_exists(db_name):
    """
    Checks if the database files for the specified database exist.
    """
    system_file = f"{db_name}_system.json"
    data_file = f"{db_name}_data.json"
    return os.path.exists(system_file) and os.path.exists(data_file)


def load_database_files(db_name):
    """
    Loads both the system and data files for the specified database.
    """
    fields = load_system_file(db_name)
    if fields is None:
        return None, None

    records = load_data_file(db_name)
    return fields, records


# Test function (optional, for demonstration)
if __name__ == "__main__":
    db_name = "example_db"
    fields = {"name": 50, "age": 3, "email": 100}

    print("Creating a database...")
    create_database_files(db_name, fields)

    print("\nLoading system file...")
    metadata = load_system_file(db_name)
    print("Metadata:", metadata)

    print("\nSaving some records...")
    save_data_file(db_name, [{"name": "Alice", "age": "25", "email": "alice@example.com"}])

    print("\nLoading data file...")
    data = load_data_file(db_name)
    print("Data:", data)

    print("\nChecking if the database exists...")
    print("Database exists:", database_exists(db_name))

    print("\nDeleting the database...")
    delete_database(db_name)
