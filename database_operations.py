import json
import os
import file_manager as fm  # Ensure to import the file manager


def delete_database(db_name):
    """Deletes the entire database by removing its data and system files."""
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"
    
    # Check if the data file exists
    if os.path.exists(data_file):
        os.remove(data_file)
        print(f"Deleted data file: {data_file}")
    else:
        print(f"Data file '{data_file}' not found.")

    # Check if the system file exists
    if os.path.exists(system_file):
        os.remove(system_file)
        print(f"Deleted system file: {system_file}")
    else:
        print(f"System file '{system_file}' not found.")

    print(f"Database '{db_name}' has been deleted successfully.")


def load_system_file(db_name):
    """Loads the system file for the specified database."""
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
    """Loads the data file for the specified database."""
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
    """Saves the records to the data file for the specified database."""
    data_file = f"{db_name}_data.json"
    try:
        with open(data_file, 'w') as f:
            json.dump(records, f, indent=4)
    except IOError as e:
        print(f"Error saving data to '{data_file}': {e}")


def add_record(db_name):
    """Adds a new record to the database."""
    fields = load_system_file(db_name)
    if not fields:
        return

    record = {}
    for field, max_length in fields.items():
        while True:
            value = input(f"Enter value for '{field}' (max {max_length} chars): ").strip()
            if len(value) > max_length:
                print(f"Value for '{field}' exceeds maximum length of {max_length}.")
            else:
                record[field] = value
                break

    records = load_data_file(db_name)
    records.append(record)
    save_data_file(db_name, records)
    print("Record added successfully.")


def view_records(db_name):
    """Displays all records in the specified database."""
    records = load_data_file(db_name)
    if not records:
        print("No records found.")
        return

    headers = list(records[0].keys())
    column_widths = {header: max(len(header), max(len(str(record.get(header, ""))) for record in records)) for header in headers}

    # Header row and separator
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    separator = "+-" + "-+-".join("-" * column_widths[header] for header in headers) + "-+"

    # Print the table
    print(separator)
    print(f"| {header_row} |")
    print(separator)
    for record in records:
        row = " | ".join(str(record.get(header, "")).ljust(column_widths[header]) for header in headers)
        print(f"| {row} |")
    print(separator)


def delete_record(db_name, record_index):
    """Deletes a record by its index from the specified database."""
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


def edit_record(db_name, record_index):
    """Edits an existing record in the specified database."""
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
