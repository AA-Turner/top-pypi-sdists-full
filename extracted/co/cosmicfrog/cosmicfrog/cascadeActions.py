import os
import json

def parse_fields(table_name, fields, mappings):
    for field in fields:
        column_name = field.get("Column Name", "")
        master_table = field.get("Master Table", "")
        master_column = field.get("MasterColumn", "")

        if master_table and master_column:
            if ", " in master_table:
                tables = master_table.split(", ")
                columns = master_column.strip('[]').split(', ')
            else:
                tables = [master_table]
                columns = [master_column]

            for table, col in zip(tables, columns):
                # Handle TableName.ColumnName format in MasterColumn
                if '.' in col:
                    col_parts = col.split('.')
                    referenced_table = col_parts[0].strip()
                    column = col_parts[1].strip()
                else:
                    referenced_table = table
                    column = col.strip()

                # Create or update the mapping structure
                if referenced_table not in mappings:
                    mappings[referenced_table] = {}
                if column not in mappings[referenced_table]:
                    mappings[referenced_table][column] = {}

                # Ensure the column name is stored as an array of strings
                if table_name not in mappings[referenced_table][column]:
                    mappings[referenced_table][column][table_name] = []
                
                # Append the column name if it doesn't exist in the list
                if column_name not in mappings[referenced_table][column][table_name]:
                    mappings[referenced_table][column][table_name].append(column_name)

def read_json_files(input_dir, output_file, anura_version):
    mappings = {}
    for filename in os.listdir(input_dir):
        if filename.startswith("anura_") and filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                parse_fields(data.get("TableName", ""), data.get("fields", []), mappings)

    with open(output_file, 'w') as file:
        json.dump(mappings, file, indent=2, sort_keys=True)

def main():
    input_dir = os.path.join(os.path.dirname(__file__), 'anura28', 'table_definitions')  # Directory containing the input JSON files
    output_file = 'output_mappings.json'  # Output JSON file path
    read_json_files(input_dir, output_file, '')
    print("Mapping file created:", output_file)

if __name__ == "__main__":
    main()
