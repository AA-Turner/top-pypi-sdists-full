"""This module contains the classes that are used to connect to resources like Warehouses, SQL databases, 
and Lakehouses. You can use these classes by importing them from the fabric.functions module 
(e.g. `from fabric.functions import FabricSqlConnection`).
"""

import json
import time
import requests
import struct
import typing
import logging

# flake8: noqa: I005
import pyodbc
from azure.storage.filedatalake import DataLakeDirectoryClient

from fabric.functions.fabric_item import FabricItem
from fabric.internal.fabric_lakehouse_files_client import FabricLakehouseFilesClient
from fabric.functions.udf_exception import UserDataFunctionInternalError
from azure.storage.filedatalake.aio import DataLakeDirectoryClient as DataLakeDirectoryClientAsync

class FabricSqlConnection(FabricItem):
    """
    This class is used to connect to resources that supply SQL connection strings.

    A User Data Function with a parameter of this type must be decorated with :meth:`fabric.functions.UserDataFunctions.connection` (see the example under `Remarks`).


    .. remarks::

        .. note::
            If you want to connect to a Lakehouse SQL endpoint, that should be done through
            :class:`FabricLakehouseClient` instead (and then use it's method :meth:`FabricLakehouseClient.connectToSql`).
        

        To use this class and have Fabric make the proper connections to your SQL endpoint, you must:
        * Add a data connection in the Connections tab of your User Data Functions on the portal.
        * Add a parameter to your User Data Function with the type 'FabricSqlConnection'.
        * Add the decorator `connection` to your User Data Function that references the parameter
        and the alias of the data connection you made.
        
        .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()
    
                @udf.connection("<data connection alias>", "<argName>")
                @udf.function()
                def my_function(<argName>: fn.FabricSqlConnection) -> None:
                    conn = <argName>.connect()
                    pass

    """

    __APPSETTINGS_PATH = "sqlendpoint"
    __INITIAL_CATALOG = "Initial Catalog"

    def _get_split_connection_string(self) -> typing.Dict[str, str]:
        connString = self.endpoints[self.__APPSETTINGS_PATH]["ConnectionString"]

        # Lakehouse connection string contains Data Source instead of Server
        connString = connString.replace("Data Source", "Server")

        if "=" not in connString:
            return {"Server": connString}

        # The reason we can't use a simple split on semi-colons is because a Fabric SQL database name can contain semi-colons.
        result = {}
        in_quotes = False
        quote_char = ""
        current_pair = []
        current_segment = []

        for char in connString:
            if char == '"' or char == "'":
                if in_quotes and char == quote_char:
                    in_quotes = False
                    quote_char = ""
                    current_segment.append(char)
                elif in_quotes:
                    current_segment.append(char)
                elif not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_segment.append(char)

            elif char == ';' and not in_quotes:
                current_segment = ''.join(current_segment).strip()
                if current_segment:
                    current_pair.append(current_segment)
                if len(current_pair) == 2:
                    key, value = current_pair

                    result[key] = value
                current_pair = []
                current_segment = []
            elif char == '=' and not in_quotes and not current_pair:
                current_segment = ''.join(current_segment).strip()
                if current_segment:
                    current_pair.append(current_segment)
                current_segment = []
            else:
                current_segment.append(char)

        # Handle the last pair
        current_segment = ''.join(current_segment).strip()
        if current_segment:
            current_pair.append(current_segment)
        if len(current_pair) == 2:
            key, value = current_pair

            result[key] = value

        if "Server" not in result:
            raise UserDataFunctionInternalError("Server value is not set in connection")

        return result

    def _modify_database_name(self, database_string: str) -> str:
        if '{' in database_string or '}' in database_string:
            raise UserDataFunctionInternalError("Databases connected to User Data Functions cannot contain '{' or '}' characters in their name.")

        # Remove surrounding quotes if present as they can interfere with the ODBC connection.
        # The database name should be passed without quote characters to the connection string, and then wrapped in curly braces.

        if database_string.startswith("\"") and database_string.endswith("\""):
            database_string = database_string[1:-1]
            # Sql databases try to escape quotes by doubling them inside double quoted strings, so we need to remove the extra quotes.
            if '""' in database_string:
                database_string = database_string.replace('""', '"')
        elif database_string.startswith("'") and database_string.endswith("'"):
            database_string = database_string[1:-1]   

        return f"Database={{{database_string}}};"

    def connect(self) -> pyodbc.Connection:
        """Connects to the SQL endpoint. Call this within your function before attempting to query the endpoint.
        """
        if self.__APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.__APPSETTINGS_PATH} is not set")
        
        dict_conn_string = self._get_split_connection_string()
        connString = dict_conn_string["Server"]

        # https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Connect-to-Azure-SQL-Database
        
        token = self.endpoints[self.__APPSETTINGS_PATH]["AccessToken"].encode('UTF-8')
        exptoken = b""
        for i in token:
            exptoken+=bytes({i})
            exptoken+=bytes(1)
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

        driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
        latest_driver = driver_names[-1] if driver_names else None

        if latest_driver is None:
            raise UserDataFunctionInternalError("No ODBC Driver found for SQL Server. Please download the latest for your OS.")

        conn_string = f'DRIVER={{{latest_driver}}};Server={connString};Encrypt=yes;LongAsMax=yes;'

        if self.__INITIAL_CATALOG in dict_conn_string:
            databaseString = self._modify_database_name(dict_conn_string[self.__INITIAL_CATALOG])     
            conn_string += databaseString
                  
        return pyodbc.connect(conn_string, attrs_before = {1256:tokenstruct}, timeout=60)

    
class FabricLakehouseClient(FabricItem):
    """This class is used to connect to Lakehouse resources. 
    You can use this class to connect to both SQL and Files endpoints.

    A User Data Function with a parameter of this type must be decorated with :meth:`fabric.functions.UserDataFunctions.connection` (see the example under `Remarks`).

    .. remarks::
        To use this class and have Fabric make the proper connections to your Lakehouse, you must:
        * Add a data connection in the Connections tab of your User Data Functions on the portal.
        * Add a parameter to your User Data Function with the type 'FabricLakehouseClient'.
        * Add the decorator `connection` to your User Data Function that references the parameter
        and the alias of the data connection you made.
        
        .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()
    
                @udf.connection("<Lakehouse alias>", "<argName>")
                @udf.function()
                def my_function(<argName>: fn.FabricLakehouseClient) -> None:
                    sql_endpoint = <argName>.connectToSql()
                    files_endpoint = <argName>.connectToFiles()
                    pass
    """

    def connectToSql(self) -> pyodbc.Connection:
        """Connects to the SQL endpoint of the Lakehouse. Call this within your function before attempting to query the endpoint.
        """

        return FabricSqlConnection(self.alias_name, self.endpoints).connect()  

    def connectToFiles(self) -> DataLakeDirectoryClient:
        """Connects to the Files endpoint of the Lakehouse. Call this within your function before attempting to query the endpoint.
        """

        return FabricLakehouseFilesClient(self.alias_name, self.endpoints).connect()
        
    def connectToFilesAsync(self) -> DataLakeDirectoryClientAsync:
        """Connects to the Files endpoint of the Lakehouse. Call this within your function before attempting to query the endpoint. Returns a client that can be used in async functions.
        """
        
        return FabricLakehouseFilesClient(self.alias_name, self.endpoints).connect_async()

class UserDataFunctionContext:
    """This class is used to be able to access certain metadata about a function invocation.

    A User Data Function with a parameter of this type must be decorated with :meth:`fabric.functions.UserDataFunctions.context` (see the example under `Remarks`).

    .. remarks::

        .. note::
            Do not use the parameter name "`context`" for this (or any) parameter in your User Data Function.

        To use this class and have Fabric generate the metadata, you must:
        * Add a parameter to your User Data Function with the type 'UserDataFunctionContext'.
        * Add the decorator `context` to your User Data Function that references the parameter.
        
        .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()
    
                @udf.context("<argName>")
                @udf.function()
                def my_function(<argName>: fn.UserDataFunctionContext) -> None:
                    invocation_id = <argName>.invocation_id
                    pass

    :param invocationId: The unique identifier for the function invocation.
    :type invocationId: str
    :param executingUser: Metadata about the user token used to execute the function.
    :type executingUser: typing.Dict[str, str]
    """
    def __init__(self, invocationId: str, executingUser: typing.Dict[str, str]):
        """Don't worry about using the constructor to create an instance of this class. Fabric will automatically create it for you (as long as you follow the steps within `Remarks`).
        """
        self.__invocation_id = invocationId
        self.__executing_user = executingUser

    @property
    def invocation_id(self) -> str:
        """The unique identifier for the function invocation.
        """

        return self.__invocation_id
    
    @property
    def executing_user(self) -> typing.Dict[str, str]:
        """Metadata about the user token used to execute the function.

        .. remarks::
            
                The dictionary contains the following keys:
                * `Oid`: The user's object id, which is an immutable identifier for the requestor, 
                which is the verified identity of the user or service principal. 
                This ID uniquely identifies the requestor across applications. 
                We suggest using this in tandem with TenantId to be the values to perform authorization checks.
                * `PreferredUsername`: The preferred username of the user, which can be an email address, 
                phone number, generic username, or unformatted string. This is mutable.
                * `TenantId`: The tenant id of the user, which represents the tenant that the user is signed into.

        """

        return self.__executing_user


class FabricVariablesClient(FabricItem):
    """
    This class is used to connect to Fabric Variable Library resources.

    A User Data Function with a parameter of this type must be decorated with :meth:`fabric.functions.UserDataFunctions.connection` (see the example under `Remarks`).

    .. remarks::
        To use this class and have Fabric make the proper connections to your Variable Library, you must:
        * Add a data connection in the Connections tab of your User Data Functions on the portal.
        * Add a parameter to your User Data Function with the type 'FabricVariablesClient'.
        * Add the decorator `connection` to your User Data Function that references the parameter
        and the alias of the data connection you made.
        
        .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()
    
                @udf.connection("<Variable Library alias>", "<argName>")
                @udf.function()
                def my_function(<argName>: fn.FabricVariablesClient) -> None:
                    variables = <argName>.getVariables()
                    pass
    """

    __APPSETTINGS_PATH = "vlendpoint"

    def getVariables(self) -> typing.Dict[str, str]:
        """Retrieves all variables from the connected Variable Library with their effective values.

        Uses the DiscoverVariablesV2 API, which returns resolved values with
        active value set overrides already applied server-side.
        
        Returns:
            dict[str, str]: A dictionary mapping variable names to their values.
        """
        if self.__APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.__APPSETTINGS_PATH} is not set")

        connection_string = self.endpoints[self.__APPSETTINGS_PATH]["ConnectionString"]
        access_token = self.endpoints[self.__APPSETTINGS_PATH]["AccessToken"]

        headers = {
            'Authorization': f'Bearer {access_token}',
            # 'content-type': 'application/json'
        }

        try:
            total_start = time.monotonic()

            # Get the variable library's display name so we can filter discover results below
            library_name = self._get_library_name(connection_string, headers)

            # Resolve all variables via DiscoverVariablesV2
            discover_url = self._build_discover_url(connection_string)
            variables = self._discover_variables(discover_url, headers, library_name)

            logging.info("Retrieved %d variable(s) from library '%s' in %.2fs total",
                         len(variables), library_name, time.monotonic() - total_start)
            return variables

        except UserDataFunctionInternalError:
            raise
        except Exception as e:
            logging.error("Failed to get variables: %s", e)
            raise UserDataFunctionInternalError(f"Exception while getting variables: {str(e)}") from e

    def _get_library_name(self, connection_string: str, headers: dict) -> str:
        """Fetch the Variable Library display name from its metadata endpoint."""
        start = time.monotonic()
        response = requests.get(connection_string, headers=headers)
        logging.info("Variable Library metadata call took %.2fs", time.monotonic() - start)

        if response.status_code != 200:
            raise UserDataFunctionInternalError(
                f"Variable Library metadata request failed: {response.status_code} - {response.text}")

        library_name = response.json().get('displayName')
        if not library_name:
            raise UserDataFunctionInternalError(
                "Variable Library displayName not found in metadata response")

        return library_name

    def _discover_variables(self, discover_url: str, headers: dict, library_name: str) -> typing.Dict[str, str]:
        """Call DiscoverVariablesV2 and return variables matching the target library."""
        variables = {}
        params = {}
        library_name_lower = library_name.lower()

        while True:
            start = time.monotonic()
            response = requests.post(discover_url, headers=headers, json={}, params=params)
            logging.info("DiscoverVariablesV2 call took %.2fs", time.monotonic() - start)

            if response.status_code != 200:
                raise UserDataFunctionInternalError(
                    f"DiscoverVariablesV2 request failed: {response.status_code} - {response.text}")

            data = response.json()
            for var in data.get('discoveredVariables', []):
                if var.get('libraryName', '').lower() == library_name_lower:
                    name = var.get('name')
                    value = var.get('value')
                    if name is not None and value is not None:
                        variables[name] = str(value)

            # Follow pagination if needed
            continuation_token = data.get('continuationToken')
            if not continuation_token:
                break
            params = {'continuationToken': continuation_token}

        return variables

    def _build_discover_url(self, connection_string: str) -> str:
        """Build the DiscoverVariablesV2 URL by extracting the workspace ID
        from the VL connection string.
        """
        url = connection_string.split('?')[0].rstrip('/')
        parts = url.split('/workspaces/')
        if len(parts) < 2:
            raise UserDataFunctionInternalError(
                "Unable to parse workspace ID from Variable Library connection string")

        base_url = parts[0]
        workspace_id = parts[1].split('/')[0]

        return f"{base_url}/workspaces/{workspace_id}/VariableLibraries/__private/discoverVariablesV2"