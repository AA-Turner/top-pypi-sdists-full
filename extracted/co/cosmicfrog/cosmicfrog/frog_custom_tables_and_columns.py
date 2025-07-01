"""
    Helper function to create, rename, delete custom tables and columns in the model
"""

import copy
import re
import json
import os
from typing import Dict, List
import requests
from .decorators import requires_parameter

PLATFORM_API_DEFAULT_TIMEOUT = 60

# TODO:
# EVENTS TO FE for refresh

ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL", "https://api.optilogic.app/v0").strip('/')


class CustomTablesAndColumns:
    """
    Helper class to create, rename, delete custom tables and columns in the model
    """

    def __init__(self, model_name: str, app_key: str, log):
        if not model_name:
            raise ValueError("Model name is required.")

        if not app_key:
            raise ValueError("App key is required.")

        if not ATLAS_API_BASE_URL:
            raise ValueError("Atlas API base URL is required.")

        self.model_name = model_name
        self._app_key = app_key
        self.log = log
        self.atlas_api_base_url = ATLAS_API_BASE_URL

    def __get_headers__(self) -> Dict[str, str]:
        return {"X-App-Key": self._app_key}

    def __validate_identifier__(self, name: str, identifier_type: str) -> bool:
        """
        Validate an identifier (table or column name).
        Raises ValueError if invalid.
        """
        regex = r"^[a-zA-Z][a-zA-Z0-9_]*$"

        if not name:
            raise ValueError(f"{identifier_type.capitalize()} name is required.")
        if not re.match(regex, name):
            raise ValueError(
                f"{identifier_type.capitalize()} name '{name}' must start with a letter and contain only letters, numbers, and underscores."
            )
        if len(name) > 63:
            raise ValueError(
                f"{identifier_type.capitalize()} name '{name}' must be less than 63 characters."
            )

        return True

    def __handle_error__(self, correlation_id, message):
        """
        Log an error and return a response
        """
        self.log.error("%s %s", correlation_id, message)
        raise ValueError(message)

    @requires_parameter("table_name")
    def create_table(self, table_name: str) -> Dict[str, str]:
        """
        Create a custom table in the model

        Args:
            table_name: str -- Name of the table to create

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Creating custom table: {table_name}")

        try:
            self.__validate_identifier__(table_name, "table")
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-table"
        data = {"tableName": table_name.lower()}
        try:
            response = requests.post(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Create table response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": f"Table '{table_name}' created successfully",
            }
        except Exception as e:
            self.log.exception(f"Error creating table: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while creating the table",
            }

    @requires_parameter("table_name")
    @requires_parameter("new_table_name")
    def rename_table(self, table_name: str, new_table_name: str) -> Dict[str, str]:
        """
        Rename a custom table in the model

        Args:
            table_name: str -- Name of the table to rename
            new_table_name: str -- New name for the table

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Renaming custom table: {table_name} to {new_table_name}")

        try:
            self.__validate_identifier__(new_table_name, "table")
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-table"
        params = {"tableName": table_name, "newTableName": new_table_name.lower()}
        try:
            response = requests.put(
                url,
                params=params,
                headers=self.__get_headers__(),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Rename table response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": f"Table '{table_name}' renamed to '{new_table_name}'",
            }
        except Exception as e:
            self.log.exception(f"Error renaming table: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while renaming the table",
            }

    @requires_parameter("table_name")
    def delete_table(self, table_name: str) -> Dict[str, str]:
        """
        Delete a custom table in the model

        Args:
            table_name: str -- Name of the table to delete

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Deleting custom table: {table_name}")

        if not table_name:
            return {"status": "error", "message": "Table name is required"}

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-table"
        data = {"tableName": table_name}
        try:
            response = requests.delete(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Delete table response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("message", ""),
            }
        except Exception as e:
            self.log.exception(f"Error deleting table: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while deleting the table",
            }

    @requires_parameter("table_name")
    def get_pk_custom_columns(self, table_name: str) -> List[str]:
        """
        Get primary key custom columns for a certain table

        Args:
            table_name: str -- Name of the table to get primary key columns for

        Returns:
            list: A list of primary key column names.
        """
        self.log.info(f"Getting primary key custom columns for table: {table_name}")
        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-columns?tableName={table_name}"
        response = requests.get(
            url, headers=self.__get_headers__(), timeout=PLATFORM_API_DEFAULT_TIMEOUT
        )

        try:
            response_data = response.json()
            if response.status_code == 200 and response_data.get("result") == "success":
                return [
                    column["columnName"]
                    for column in response_data.get("customColumns", [])
                    if column.get("isTableKeyColumn", True)
                ]

            self.log.error(f"Error: {response_data.get('message')}")
            return []
        except Exception as e:
            self.log.error(f"An error occurred fetching custom column PKs: {str(e)}")
            return []

    def get_custom_tables(self) -> List[str]:
        """
        Get all custom tables in the model

        Returns:
            list: A list of custom table names.
        """

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-tables"
        response = requests.get(
            url, headers=self.__get_headers__(), timeout=PLATFORM_API_DEFAULT_TIMEOUT
        )

        try:
            response_data = response.json()
            if response.status_code == 200 and response_data.get("result") == "success":
                return response_data.get("customTables", [])

            self.log.error(f"Error: {response_data.get('message')}")
            return []
        except Exception as e:
            self.log.error(f"An error occurred fetching custom tables: {str(e)}")
            return []

    @requires_parameter("table_name")
    def get_all_custom_columns(self, table_name) -> Dict[str, str]:
        """
        Get all custom columns for a certain table

        Args:
            table_name: str -- Name of the table to get custom columns for

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """

        self.log.info(f"Getting all custom columns for table: {table_name}")
        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-columns"
        data = {"tableName": table_name}
        try:
            response = requests.request(
                "GET",
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Get all custom columns response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("customColumns", ""),
            }
        except Exception as e:
            self.log.exception(f"Error getting custom columns: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while getting custom columns",
            }

    @requires_parameter("table_name")
    @requires_parameter("column_name")
    def create_custom_column(
        self,
        table_name: str,
        column_name: str,
        data_type: str = "text",
        key_column: bool = False,
        pseudo: bool = True,
    ) -> Dict[str, str]:
        """
        Create a custom column in a custom table

        Args:
            table_name: str -- Name of the table to create the column in
            column_name: str -- Name of the column to create
            data_type: str -- Data type of the column (e.g. text, integer, float, date, bool)
            key_column: bool -- Will be included as part of the unique record identification when importing (updating, inserting) data to the table
            pseudo: bool -- Data of any type can be freely imported and will behave as the defined data type in UI (Grids, Maps, Dashboards)

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Creating custom column: {column_name} in table: {table_name}")
        if not table_name:
            return {"status": "error", "message": "Table name is required"}

        if not column_name:
            return {"status": "error", "message": "Column name is required"}

        try:
            self.__validate_identifier__(column_name, "column")
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        if not data_type:
            return {"status": "error", "message": "Data type is required"}

        if pseudo:
            true_data_type = "text"
        else:
            true_data_type = data_type

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-column"
        data = {
            "tableName": table_name.lower(),
            "columnName": column_name.lower(),
            "dataType": data_type,
            # 'characterMaximumLength': 255,
            # 'isNullable': False,
            # 'defaultValue': None,
            "isTableKeyColumn": key_column,
            "trueDataType": true_data_type,
            # 'isRequired': True
        }

        try:
            response = requests.post(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Create custom column response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("message", ""),
            }
        except Exception as e:
            self.log.exception(f"Error creating custom column: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while creating the custom column",
            }


    @requires_parameter("columns")
    def bulk_create_custom_columns(
        self, columns: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Bulk create custom columns.

        Each column should be a dictionary with the following keys:
            - table_name: str
            - column_name: str
            - data_type: str (Optional) - Default is 'text'
            - key_column: bool (Optional) - Default is False
            - pseudo: bool (Optional) - Default is True

        Example Args:
            columns = [
                {
                    "table_name": "Facilities",
                    "column_name": "Custom1",
                    "data_type": "integer",
                },
                {
                    "table_name": "Facilities",
                    "column_name": "Custom2"
                },
                {
                    "table_name": "Customers",
                    "column_name": "Custom3",
                }
            ]

        Args:
            columns: list -- List of columns to create
        
        Returns:
            dict: A dictionary containing 'status', 'message', 'added', 'skipped', and 'errors'.
        """
        self.log.info(f"Bulk creating custom columns: {columns}")

        local_columns = copy.deepcopy(columns)

        for column in local_columns:
            if not column.get("table_name"):
                return {"status": "error", "message": f"Table name is required. Error found in column: {column}"}

            if not column.get("column_name"):
                return {"status": "error", "message": f"Column name is required, Error found in column: {column}"}

            try:
                self.__validate_identifier__(column.get("column_name"), "column")
            except ValueError as e:
                return {"status": "error", "message": str(e)}

            if not column.get("data_type"):
                column["dataType"] = "text"
            else:
                column["dataType"] = column.get("data_type")
                column.pop("data_type", None)
            
            column["tableName"] = column.get("table_name").lower()
            column.pop("table_name", None)

            column["columnName"] = column.get("column_name").lower()
            column.pop("column_name", None)

            if column.get("pseudo"):
                column["trueDataType"] = "text"
                column.pop("pseudo", None)
            else:
                column["trueDataType"] = column["dataType"]
                column.pop("pseudo", None)

            if column.get("key_column"):
                column["isTableKeyColumn"] = column.get("key_column")
                column.pop("key_column", None)

        data = {
            "columns": local_columns
        }

        try:
            url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-columns"
            response = requests.post(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Bulk create custom columns response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("message", ""),
                "added": res.get("added", []),
                "skipped": res.get("skipped", []),
                "errors": res.get("errors", []),
            }
        except Exception as e:
            self.log.exception(f"Error bulk creating custom columns: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while bulk creating custom columns",
            }


    @requires_parameter("table_name")
    @requires_parameter("column_name")
    def delete_custom_column(self, table_name: str, column_name: str) -> Dict[str, str]:
        """
        Delete a custom column in a custom table

        Args:
            table_name: str -- Name of the table to delete the column from
            column_name: str -- Name of the column to delete

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Deleting custom column: {column_name} from table: {table_name}")
        if not table_name:
            return {"status": "error", "message": "Table name is required"}

        if not column_name:
            return {"status": "error", "message": "Column name is required"}

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-column"
        data = {"tableName": table_name, "columnName": column_name}
        try:
            response = requests.delete(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = response.json()
            self.log.info(f"Delete custom column response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("message", ""),
            }
        except Exception as e:
            self.log.exception(f"Error deleting custom column: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while deleting the custom column",
            }

    @requires_parameter("table_name")
    @requires_parameter("column_name")
    def edit_custom_column(
        self,
        table_name: str,
        column_name: str,
        new_column_name: str = None,
        data_type: str = None,
        key_column: bool = None,
    ) -> Dict[str, str]:
        """
        Edit a custom column in a custom table

        Args:
            table_name: str -- Name of the table to edit the column in
            column_name: str -- Name of the column to edit
            new_column_name: str -- New name of the column
            data_type: str -- New data type of the column (e.g. text, integer, float, date, boolean)
            key_column: bool -- Will be included as part of the unique record identification when importing (updating, inserting) data to the table
            pseudo: bool -- Data of any type can be freely imported and will behave as the defined data type in UI (Grids, Maps, Dashboards)

        Returns:
            dict: A dictionary containing 'status' and 'message'.
        """
        self.log.info(f"Editing custom column: {column_name} in table: {table_name}")
        if not table_name:
            return {"status": "error", "message": "Table name is required"}

        if not column_name:
            return {"status": "error", "message": "Column name is required"}

        try:
            if new_column_name:
                self.__validate_identifier__(new_column_name, "new_column_name")
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        url = f"{self.atlas_api_base_url}/storage/{self.model_name}/custom-column"
        data = {"tableName": table_name.lower(), "columnName": column_name}
        if new_column_name:
            data["newColumnName"] = new_column_name.lower()
        if data_type:
            data["dataType"] = data_type
            data["trueDataType"] = data_type
        if key_column is not None:
            data["isTableKeyColumn"] = key_column

        try:
            request = requests.put(
                url,
                headers=self.__get_headers__(),
                data=json.dumps(data),
                timeout=PLATFORM_API_DEFAULT_TIMEOUT,
            )
            res = request.json()
            self.log.info(f"Edit custom column response: {res}")

            return {
                "status": res.get("result", "error"),
                "message": res.get("message", ""),
            }
        except Exception as e:
            self.log.exception(f"Error editing custom column: {e}", exc_info=True)
            return {
                "status": "error",
                "message": "An error occurred while editing the custom column",
            }
