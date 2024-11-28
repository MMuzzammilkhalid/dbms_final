# Importing necessary modules for database operations.
# The `json` module is used to handle JSON files for reading and writing database data and system files.
# The `os` module is used to manage file operations like checking file existence and deletion.
# The `file_manager` module is used to assist in file-related tasks specific to this application.
import json
import os
import file_manager as fm  # Ensure to import the file manager for managing database files.

# This function deletes an entire database by removing both its data and system files from the file system.
# It first verifies the existence of the respective files and deletes them if they are found. 
# If the files are not found, it notifies the user and ensures no unnecessary errors occur.
def delete_database(db_name):
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

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

# This function loads the system file of a specified database, which contains metadata about the database's structure,
# such as field names and their maximum lengths. If the file doesn't exist or is corrupted, it handles the error 
# gracefully and returns `None`.
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

# This function loads the data file of a specified database, which contains all the records stored in the database.
# If the file doesn't exist or is corrupted, it notifies the user and returns an empty list as a fallback.
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

# This function saves a list of records to the data file of a specified database. 
# It writes the data in JSON format and handles any file I/O errors during the process, notifying the user if an issue occurs.
def save_data_file(db_name, records):
    data_file = f"{db_name}_data.json"
    try:
        with open(data_file, 'w') as f:
            json.dump(records, f, indent=4)
    except IOError as e:
        print(f"Error saving data to '{data_file}': {e}")

# This function enables the user to add a new record to a database. It prompts the user for values for each field defined 
# in the system file, validates the input lengths, and appends the new record to the data file. If any required file is missing, 
# it gracefully handles the error.
def add_record(db_name):
    fields = load_system_file(db_name)
    if not fields:
        return

    record = {}
    for field, max_length in fields.items():
        while True:
            value = input(f"Enter value for '{field}' (max {max_length} chars): ").strip()
            if not value:
                print(f"Error: '{field}' cannot be empty. Please enter a value.")
            elif len(value) > max_length:
                print(f"Value for '{field}' exceeds maximum length of {max_length}.")
            else:
                record[field] = value
                break

    if not record:  # If no valid record is added, show an appropriate message
        print("No valid data entered. Record not added.")
    else:
        records = load_data_file(db_name)
        records.append(record)
        save_data_file(db_name, records)
        print("Record added successfully.")

# This function displays all the records stored in a database in a tabular format. 
# It calculates the column widths dynamically to ensure proper alignment of data. If no records are found, it notifies the user.
def view_records(db_name):
    records = load_data_file(db_name)
    if not records:
        print("No records found.")
        return

    headers = list(records[0].keys())
    column_widths = {header: max(len(header), max(len(str(record.get(header, ""))) for record in records)) for header in headers}

    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    separator = "+-" + "-+-".join("-" * column_widths[header] for header in headers) + "-+"

    print(separator)
    print(f"| {header_row} |")
    print(separator)
    for record in records:
        row = " | ".join(str(record.get(header, "")).ljust(column_widths[header]) for header in headers)
        print(f"| {row} |")
    print(separator)

# This function allows the user to delete a specific record from a database by its index. 
# It confirms the deletion with the user and removes the record if the index is valid. If no records are found or the index 
# is invalid, it handles the error gracefully.
def delete_record(db_name, record_index):
    records = load_data_file(db_name)
    if not records:
        print("No records found.")
        return

    if 0 <= record_index < len(records):
        confirm = input(f"Are you sure you want to delete record {record_index + 1}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            records.pop(record_index)
            save_data_file(db_name, records)
            print(f"Record {record_index + 1} deleted successfully.")
        else:
            print("Deletion canceled.")
    else:
        print("Invalid record index.")

# This function enables the user to edit an existing record in a database by specifying its index. 
# The user can update values for each field while ensuring input lengths adhere to the defined constraints. 
# If the record index is invalid or required files are missing, it handles the situation gracefully.
def edit_record(db_name, record_index):
    fields = load_system_file(db_name)
    records = load_data_file(db_name)

    if not fields or not records:
        return

    if 0 <= record_index < len(records):
        record = records[record_index]
        print(f"Editing record {record_index + 1}:")
        for field, max_length in fields.items():
            current_value = record.get(field, "")
            while True:
                new_value = input(f"{field} [{current_value}]: ").strip() or current_value
                if len(new_value) > max_length:
                    print(f"Value for '{field}' exceeds maximum length of {max_length}.")
                else:
                    record[field] = new_value
                    break
        save_data_file(db_name, records)
        print("Record updated successfully.")
    else:
        print("Invalid record index.")
