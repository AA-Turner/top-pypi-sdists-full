# flake8: noqa: I900, R504
from urllib.parse import urlparse

from azure.storage.filedatalake import DataLakeDirectoryClient
from azure.storage.filedatalake.aio import DataLakeDirectoryClient as DataLakeDirectoryClientAsync

from fabric.internal.custom_token_credential import \
    CustomTokenCredential
from fabric.functions.fabric_item import FabricItem
from fabric.functions.udf_exception import UserDataFunctionInternalError


class FabricLakehouseFilesClient(FabricItem):
    """
    This class is used to connect to resources that supply Lakehouse file connection strings.

    .. remarks::

        .. note::
            If you want to connect to a Lakehouse Files endpoint, that should be done through
            :class:`FabricLakehouseClient` instead (and then use it's method :meth:`FabricLakehouseClient.connectToFiles`).

    """

    __APPSETTINGS_PATH = "fileendpoint"

    def connect(self) -> DataLakeDirectoryClient:
        """Makes a connection to the Lakehouse Files endpoint. Call this within your function.
        """
        if self.__APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.__APPSETTINGS_PATH} is not set")

        raw_path = self.endpoints[self.__APPSETTINGS_PATH]['ConnectionString']
        parsed_path = urlparse(raw_path)

        access_token = self.endpoints[self.__APPSETTINGS_PATH]['AccessToken']

        # The account URL is the scheme and netloc parts of the parsed path
        account_url = f"{parsed_path.scheme}://{parsed_path.netloc}"

        # The file system name and directory name are in the path part of the parsed path
        # We remove the leading slash and then split the rest into the file system name
        # and directory name
        file_system_name, _, directory_name = parsed_path.path.lstrip('/').partition('/')

        directory_client = DataLakeDirectoryClient(account_url, file_system_name, directory_name,
                                                    CustomTokenCredential(access_token))
        return directory_client

    def connect_async(self) -> DataLakeDirectoryClientAsync:
        """Makes a connection to the Lakehouse Files endpoint. Call this within your function. Returns a client that can be used in async functions.
        """
        if self.__APPSETTINGS_PATH not in self.endpoints:
            raise UserDataFunctionInternalError(f"{self.__APPSETTINGS_PATH} is not set")

        raw_path = self.endpoints[self.__APPSETTINGS_PATH]['ConnectionString']
        parsed_path = urlparse(raw_path)

        access_token = self.endpoints[self.__APPSETTINGS_PATH]['AccessToken']

        # The account URL is the scheme and netloc parts of the parsed path
        account_url = f"{parsed_path.scheme}://{parsed_path.netloc}"

        # The file system name and directory name are in the path part of the parsed path
        # We remove the leading slash and then split the rest into the file system name
        # and directory name
        file_system_name, _, directory_name = parsed_path.path.lstrip('/').partition('/')

        directory_client = DataLakeDirectoryClientAsync(account_url, file_system_name, directory_name,
                                                    CustomTokenCredential(access_token))
        return directory_client
