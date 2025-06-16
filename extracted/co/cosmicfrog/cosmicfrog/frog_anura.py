"""
Module holding AnuraSchema class
"""

import os
from typing import List, Dict, Tuple
import importlib.resources
import json
from cachetools import cached, LRUCache

# Hold supported schema versions, and maps to the directory in which they are stored
# Key: schema from model db
# Value: json folder
SUPPORTED_SCHEMAS = {
    "anura_2_7": "anura27",
    "anura_2_8": "anura28",
    "stable": "anura27",
    "preview": "anura28",
}

LIBRARY_NAME = "cosmicfrog"


class AnuraSchema:
    """
    Static class for managing Anura schema versions
    """

    def __init__(self):
        raise RuntimeError("Do not instantiate directly - Static class")

    @staticmethod
    @cached(LRUCache(maxsize=len(SUPPORTED_SCHEMAS)))
    def get_anura_masterlist(anura_version: str) -> List:
        """
        Return the masterlist for the given Anura schema

        """
        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/anuraMasterTableList.json"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Fetch all table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            table_name = field["Table"]
            result.append(table_name)

        if lower_case:
            return [s.lower() for s in result]

        return result

    @staticmethod
    def get_anura_abreviated_table_names(anura_version: str, input_only: bool = False) -> Dict[str, str]:
        """
        Fetch all abbreviated table names and create a dictionary with table names
        """

        result = {}

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            if input_only and field["Category"].startswith("Output"):
                continue
            table_name = field["Table"].lower()
            abbreviated_name = field["AbbreviatedName"].lower()

            result[abbreviated_name] = table_name

        return result

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_input_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Fetch input table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            if field["Category"].startswith("Output") is False:
                result.append(field["Table"])

        if lower_case:
            return [s.lower() for s in result]

        return result

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_output_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Return output  table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            if field["Category"].startswith("Output"):
                result.append(field["Table"])

        if lower_case:
            return [s.lower() for s in result]

        return result

    @staticmethod
    def get_anura_keys(anura_version: str, table_name: str) -> List[str]:
        """
        Get table keys defined in Anura schema
        """

        anura_keys, _ = AnuraSchema._get_anura_key_and_column_dicts(anura_version)

        return anura_keys.get(table_name, [])

    @staticmethod
    def get_anura_columns(anura_version: str, table_name: str) -> List[str]:
        """
        Get table coluimns defined in Anura schema
        """
        _, anura_columns = AnuraSchema._get_anura_key_and_column_dicts(anura_version)

        return anura_columns.get(table_name, [])

    @staticmethod
    @cached(LRUCache(maxsize=2))
    def _get_anura_key_and_column_dicts(
        anura_version: str,
    ) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Extract keys and columns from json definitions
        """

        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/table_definitions"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:

            anura_keys = {}
            anura_cols = {}

            # Iterate over each file in the directory
            for filename in os.listdir(file_path):

                if not filename.endswith(".json"):
                    continue

                filepath = os.path.join(file_path, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                table_name = data.get("TableName").lower()

                # Extract the column names where "PK" is "Yes"
                anura_cols[table_name] = [
                    field["Column Name"].lower() for field in data.get("fields", [])
                ]
                anura_keys[table_name] = [
                    field["Column Name"].lower()
                    for field in data.get("fields", [])
                    if field.get("PK") == "Yes"
                ]

            return anura_keys, anura_cols

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_master_table_mappings(anura_version: str):
        """
        Return the master table mappings for the given Anura schema
        """

        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/anuraMasterTablesMappings.json"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

    # DEPRECATED remove in next version 1.0.5
    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_validations(
        anura_version: str,
        lower_case: bool = True
    ) -> Dict[str, List[Dict]]:
        """
        Returns validation mappings for all tables in schema.
        
        Args:
            anura_version: Schema version to use
            lower_case: Convert table and column names to lowercase
        
        Returns:
            Dictionary mapping table names to their validation rules:
            {
                "table_name": [
                    {
                        "column": "column_name",
                        "validation_type": "validation_type",
                        "field_info": {
                            "Column Name": str,
                            "Data Type": str,
                            "Validation Type": str,
                            "Required": str,
                            ...
                        }
                    },
                    ...
                ]
            }
        """
        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/table_definitions"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            validation_mappings = {}

            for filename in os.listdir(file_path):
                if not filename.endswith('.json'):
                    continue

                filepath = os.path.join(file_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                table_name = data.get('TableName', '')
                if not table_name:
                    continue

                if lower_case:
                    table_name = table_name.lower()

                validations = []
                for field in data.get('fields', []):
                    if field.get('Validation Type'):
                        validation_entry = {
                            "column": field.get('Column Name', ''),
                            "validation_type": field['Validation Type'],
                            "field_info": field.copy()
                        }
                        
                        if lower_case:
                            validation_entry["column"] = validation_entry["column"].lower()
                        
                        validations.append(validation_entry)

                if validations:
                    validation_mappings[table_name] = validations

            return validation_mappings
        
    # DEPRECATED remove in next version 1.0.5
    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_validation_types(anura_version: str) -> Dict[str, int]:
        """
        Returns all unique validation types and their frequency of use.
        
        Args:
            anura_version: Schema version to use
        
        Returns:
            Dictionary of validation types and their counts:
            {
                "validation_type": count,
                ...
            }
        """
        validation_counts = {}
        mappings = AnuraSchema.get_anura_validations(anura_version)
        
        for table_validations in mappings.values():
            for validation in table_validations:
                val_type = validation["validation_type"]
                validation_counts[val_type] = validation_counts.get(val_type, 0) + 1
                
        return dict(sorted(
            validation_counts.items(),
            key=lambda x: (-x[1], x[0])  # Sort by count desc, then name
        ))

    # DEPRECATED remove in next version 1.0.5
    @staticmethod
    def get_table_validations(
        table_name: str,
        anura_version: str,
        lower_case: bool = True
    ) -> List[Dict]:
        """
        Returns validations for a specific table.
        
        Args:
            table_name: Name of the table to get validations for
            anura_version: Schema version to use
            lower_case: Convert table and column names to lowercase
        
        Returns:
            List of validation rules for the table
        """
        if lower_case:
            table_name = table_name.lower()

        mappings = AnuraSchema.get_anura_validations(anura_version, lower_case)
        return mappings.get(table_name, [])
    

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_field_definitions(
        anura_version: str,
        lower_case: bool = True,
        input_only: bool = False
    ) -> Dict[str, List[Dict]]:
        """
        Returns all field definitions from the schema, including Data Type and Validation Type.
        
        Args:
            anura_version: Schema version to use
            lower_case: Convert table and column names to lowercase
            input_only: If True, only include input tables (exclude output tables)
            
        Returns:
            Dictionary mapping table names to their field definitions:
            {
                "table_name": [
                    {
                        "Column Name": str,
                        "Data Type": str,
                        "Validation Type": str,
                        ... (all other field properties)
                    },
                    ...
                ]
            }
        """
        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/table_definitions"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            field_definitions = {}

            # Get input tables if needed for filtering
            input_tables = set()
            if input_only:
                input_tables = set(AnuraSchema.get_anura_input_table_names(anura_version, lower_case=True))

            for filename in os.listdir(file_path):
                if not filename.endswith('.json'):
                    continue

                filepath = os.path.join(file_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                table_name = data.get('TableName', '')
                if not table_name:
                    continue
                    
                # Skip if we're only looking for input tables and this isn't one
                if input_only and table_name.lower() not in input_tables:
                    continue

                # Format table name based on case preference
                if lower_case:
                    table_key = table_name.lower()
                else:
                    table_key = table_name
                    
                # Get field definitions
                fields = data.get('fields', [])
                
                # Store the field definitions
                field_definitions[table_key] = fields

            return field_definitions
        
    @staticmethod
    def get_table_field_definitions(
        table_name: str,
        anura_version: str,
        lower_case: bool = True
    ) -> List[Dict]:
        """
        Returns complete field definitions for a specific table, including Data Type and Validation Type.
        
        Args:
            table_name: Name of the table to get field definitions for
            anura_version: Schema version to use
            lower_case: Convert table and column names to lowercase
        
        Returns:
            List of field definitions for the table, each containing data type and validation information
        """
        if lower_case:
            table_name = table_name.lower()
            
        all_definitions = AnuraSchema.get_anura_field_definitions(anura_version, lower_case)
        return all_definitions.get(table_name, [])