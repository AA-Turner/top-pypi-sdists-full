from abc import ABC, abstractmethod
from .shipyard_logger import ShipyardLogger
from .exit_code_exception import ExitCodeException
from typing import Optional


class UploadError(ExitCodeException):
    def __init__(self, table: str, error_msg: Exception):
        self.message = (
            f"Error in loading data to {table}. Message from the server is: {error_msg}"
        )
        self.exit_code = Database.EXIT_CODE_UPLOAD_ERROR


class FetchError(ExitCodeException):
    def __init__(self, error_msg: Exception):
        self.message = (
            f"Error in downloading data. Message from the server is: {error_msg}"
        )
        self.exit_code = Database.EXIT_CODE_DOWNLOAD_ERROR


class QueryError(ExitCodeException):
    def __init__(self, error_msg: Exception):
        self.message = (
            f"Error in executing query. Message from the server is: {error_msg}"
        )
        self.exit_code = Database.EXIT_CODE_QUERY_ERROR


class ConnectionError(ExitCodeException):
    def __init__(self, message: str):
        self.message = message
        self.exit_code = Database.EXIT_CODE_INVALID_CREDENTIALS


class Database(ABC):
    EXIT_CODE_INVALID_CREDENTIALS = 200
    EXIT_CODE_INVALID_ACCOUNT = 201  # snowflake specific
    EXIT_CODE_INVALID_WAREHOUSE = 202
    EXIT_CODE_INVALID_DATABASE = 203
    EXIT_CODE_INVALID_SCHEMA = 204
    EXIT_CODE_INVALID_QUERY = 205
    EXIT_CODE_NO_RESULTS = 206
    EXIT_CODE_INVALID_UPLOAD_COLUMNS = 207
    EXIT_CODE_INVALID_ARGUMENTS = 208
    EXIT_CODE_INVALID_DATA_TYPES = 209
    EXIT_CODE_FILE_NOT_FOUND = 210
    EXIT_CODE_INVALID_UPLOAD_VALUE = 211
    EXIT_CODE_NO_FILE_MATCHES = 212

    # method errors
    EXIT_CODE_UPLOAD_ERROR = 220
    EXIT_CODE_QUERY_ERROR = 221
    EXIT_CODE_DOWNLOAD_ERROR = 222

    EXIT_CODE_UNKNOWN = 249

    def __init__(self, username: str, password: Optional[str] = None, **kwargs) -> None:
        self.username = username
        self.password = password

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, **kwargs):
        pass

    @abstractmethod
    def fetch(self, **kwargs):
        pass

    @abstractmethod
    def upload(self, **kwargs):
        pass


class GoogleDatabase:
    EXIT_CODE_INVALID_CREDENTIALS = 200
    EXIT_CODE_INVALID_ACCOUNT = 201  # snowflake specific
    EXIT_CODE_INVALID_WAREHOUSE = 202
    EXIT_CODE_INVALID_DATABASE = 203
    EXIT_CODE_INVALID_SCHEMA = 204  # snowflake specific
    EXIT_CODE_INVALID_QUERY = 205
    EXIT_CODE_NO_RESULTS = 206
    EXIT_CODE_FILE_NOT_FOUND = 205
    EXIT_CODE_INVALID_UPLOAD_VALUE = 206
    EXIT_CODE_INVALID_UPLOAD_COLUMNS = 207
    EXIT_CODE_INVALID_ARGUMENTS = 208
    EXIT_CODE_INVALID_DATA_TYPES = 209

    def __init__(self, service_account: str, **kwargs) -> None:
        self.service_account = service_account

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, **kwargs):
        pass

    @abstractmethod
    def fetch(self, **kwargs):
        pass

    @abstractmethod
    def upload(self, **kwargs):
        pass


class DatabricksDatabase:
    EXIT_CODE_INVALID_CREDENTIALS = 200
    EXIT_CODE_INVALID_WAREHOUSE = 202
    EXIT_CODE_INVALID_DATABASE = 203
    EXIT_CODE_INVALID_SCHEMA = 204
    EXIT_CODE_INVALID_QUERY = 205
    EXIT_CODE_NO_RESULTS = 206
    EXIT_CODE_FILE_NOT_FOUND = 205
    EXIT_CODE_INVALID_UPLOAD_VALUE = 206
    EXIT_CODE_INVALID_UPLOAD_COLUMNS = 207
    EXIT_CODE_INVALID_ARGUMENTS = 208
    EXIT_CODE_INVALID_DATA_TYPES = 209
    EXIT_CODE_INSERT_STATEMENT_ERROR = 210
    EXIT_CODE_CREATE_STATEMENT_ERROR = 211
    EXIT_CODE_UNKNOWN_ERROR = 249

    def __init__(
        self, server_host: str, http_path: str, access_token: str, **kwargs
    ) -> None:
        self.server_host = server_host
        self.http_path = http_path
        self.access_token = access_token

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, **kwargs):
        pass

    @abstractmethod
    def fetch(self, **kwargs):
        pass

    @abstractmethod
    def upload(self, **kwargs):
        pass
