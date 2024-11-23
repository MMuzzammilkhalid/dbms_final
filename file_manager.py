# Importing necessary modules for managing database files.
# The `json` module is used to read and write data in JSON format, enabling structured storage and retrieval.
# The `os` module is used for file system operations such as checking for file existence and deleting files.
import json
import os


# This function deletes a database by removing its associated data and system files.
# It ensures both the data file (storing records) and the system file (storing metadata) are deleted if they exist.
# If a file is not found or an error occurs during deletion, the function handles it gracefully and notifies the user.
def delete_database(db_name):
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

    try:
        if os.path.exists(data_file):
            os.remove(data_file)
            print(f"Deleted data file: {data_file}")
        else:
            print(f"Data file '{data_file}' not found.")

        if os.path.exists(system_file):
            os.remove(system_file)
            print(f"Deleted system file: {system_file}")
        else:
            print(f"System file '{system_file}' not found.")

        print(f"Database '{db_name}' has been deleted successfully.")
    except Exception as e:
        print(f"Error deleting database '{db_name}': {e}")


# This function creates the necessary files for a new database.
# The system file stores metadata about the database (e.g., field names and maximum lengths), while the data file is
# initialized as an empty list to store records. If file creation fails, it returns a failure indication.
def create_database_files(db_name, fields):
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


# This function loads the system file of a database, which contains its metadata (e.g., field definitions and constraints).
# If the file does not exist or is corrupted, it handles the situation gracefully by returning `None` and notifying the user.
def load_system_file(db_name):
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


# This function loads the data file of a database, which stores the records in JSON format.
# If the file does not exist, it returns an empty list. It also handles file corruption by notifying the user
# and returning an empty list as a fallback.
def load_data_file(db_name):
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


# This function saves a list of records to the data file of a database.
# It ensures data is written in a structured JSON format, and any I/O errors during the save process
# are caught and reported to the user.
def save_data_file(db_name, records):
    data_file = f"{db_name}_data.json"

    try:
        with open(data_file, 'w') as f:
            json.dump(records, f, indent=4)
        print(f"Records saved successfully to '{db_name}'.")
    except IOError as e:
        print(f"Error saving records to '{db_name}_data.json': {e}")


# This function checks whether the necessary files for a database (data and system files) exist.
# It returns `True` if both files are found, indicating that the database is intact; otherwise, it returns `False`.
def database_exists(db_name):
    system_file = f"{db_name}_system.json"
    data_file = f"{db_name}_data.json"
    return os.path.exists(system_file) and os.path.exists(data_file)


# This function loads both the system file (metadata) and data file (records) for a specified database.
# It returns the metadata and records if successful. If the system file is missing or corrupted, it returns
# `None` for both and notifies the user.
def load_database_files(db_name):
    fields = load_system_file(db_name)
    if fields is None:
        return None, None

    records = load_data_file(db_name)
    return fields, records


# The following block demonstrates the usage of these functions.
# It creates a test database, performs basic operations, and demonstrates database management tasks.
if __name__ == "__main__":
    db_name = "example_db"
    fields = {"name": 50, "age": 3, "email": 100}  # Field definitions with maximum lengths

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
