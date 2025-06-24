import logging
import os
from datetime import datetime
from google.cloud.logging import Client
from google.cloud.logging.handlers import CloudLoggingHandler
from google.oauth2.service_account import Credentials
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Union
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.loaders.credential.google import GoogleCredentialsLoader

class GoogleCloudLogging:
    def __init__(
        self,
        credentials_path: Optional[Union[Path, str]] = None
    ) -> None:
        self._credentials = GoogleCredentialsLoader.load(credentials_path=credentials_path)
        self._client = Client(credentials=self._credentials)
        self._client.setup_logging()

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @property
    def client(self) -> Client:
        return self._client

    def dispose(self) -> None:
        if self._credentials is not None:
            self._credentials = None
        if self._client is not None:
            self._client = None

    def create_handler(
        self,
        name: str
    ) -> CloudLoggingHandler:
        return CloudLoggingHandler(client=self._client, name=name)

class SimpleConfig(BaseModel):
    dir: str = Field(..., description="Log's directory")
    level: BaseEnums.LoggerLevel = Field(BaseEnums.LoggerLevel.INFO, description="Log's level")
    google_cloud_logging: Optional[GoogleCloudLogging] = Field(default_factory=GoogleCloudLogging, description="Google cloud logging")

    class Config:
        arbitrary_types_allowed=True

class BaseLogger(logging.Logger):
    def __init__(
        self,
        dir: str,
        type: BaseEnums.LoggerType,
        service_key: BaseTypes.OptionalString = None,
        middleware_type: Optional[BaseEnums.MiddlewareLoggerType] = None,
        client_key: BaseTypes.OptionalString = None,
        level: BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO,
        google_cloud_logging: Optional[GoogleCloudLogging] = None
    ):
        self._type = type #* Declare logger type

        #* Ensure service_key exists
        self._service_key = service_key or os.getenv("SERVICE_KEY")
        if self._service_key is None:
            raise ValueError("SERVICE_KEY environment variable must be set if 'service_key' is set to None")

        self._middleware_type = middleware_type #* Declare middleware type

        if self._type == BaseEnums.LoggerType.MIDDLEWARE and self._middleware_type is None:
            raise ValueError("'middleware_type' parameter must be provided if 'logger_type' is 'middleware'")

        self._client_key = client_key #* Declare client key

        #* Ensure client_key is valid if logger type is a client
        if self._type == BaseEnums.LoggerType.CLIENT and self._client_key is None:
            raise ValueError("'client_key' parameter must be provided if 'logger_type' is 'client'")

        #* Define logger name
        if self._type == BaseEnums.LoggerType.CLIENT:
            #* Ensure client_key is valid if logger type is client
            if self._client_key is None:
                raise ValueError("'client_key' parameter must be provided if 'logger_type' is 'client'")
            self._name = f"{self._service_key} - {self._type} - {self._client_key}"
        elif self._type == BaseEnums.LoggerType.MIDDLEWARE:
            #* Ensure middleware_type is valid if logger type is middleware
            if self._middleware_type is None:
                raise ValueError("'middleware_type' parameter must be provided if 'logger_type' is 'middleware'")
            self._name = f"{self._service_key} - {self._type} - {self._middleware_type}"
        else:
            self._name = f"{self._service_key} - {self._type}"

        super().__init__(self._name, level) #* Init the superclass's logger

        #* Clear existing handlers to prevent duplicates
        for handler in list(self.handlers):
            self.removeHandler(handler)
            handler.close()

        #* Formatter for logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        #* Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        #* Google Cloud Logging handler (If enabled)
        if google_cloud_logging is not None:
            cloud_logging_handler = google_cloud_logging.create_handler(name=self._name.replace(" ", ""))
            self.addHandler(cloud_logging_handler)
        else:
            self.info("Cloud logging is not configured.")

        #* Define log directory
        if self._type == BaseEnums.LoggerType.MIDDLEWARE:
            log_dir = f"{self._type}/{self._middleware_type}"
        elif self._type == BaseEnums.LoggerType.CLIENT:
            log_dir = f"{self._type}/{self._client_key}"
        else:
            log_dir = f"{self._type}"
        self._log_dir = os.path.join(dir, log_dir)
        os.makedirs(self._log_dir, exist_ok=True)

        #* Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(self._log_dir, f"{timestamp}.log")

        #* File handler
        file_handler = logging.FileHandler(log_filename, mode="a")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    @property
    def type(self) -> str:
        return self._type

    @property
    def service(self) -> str:
        return self._service_key

    @property
    def client(self) -> str:
        raise NotImplementedError()

    @property
    def identity(self) -> str:
        return self._name

    @property
    def location(self) -> str:
        return self._log_dir

    def dispose(self):
        """Dispose of the logger by removing all handlers."""
        for handler in list(self.handlers):
            self.removeHandler(handler)
            handler.close()
        self.handlers.clear()

class MiddlewareLogger(BaseLogger):
    def __init__(
        self,
        dir: str,
        service_key: BaseTypes.OptionalString = None,
        middleware_type = None,
        level = BaseEnums.LoggerLevel.INFO,
        google_cloud_logging = None
    ):
        super().__init__(
            dir=dir,
            type=BaseEnums.LoggerType.MIDDLEWARE,
            service_key=service_key,
            middleware_type=middleware_type,
            client_key=None,
            level=level,
            google_cloud_logging=google_cloud_logging
        )

class ServiceLogger(BaseLogger):
    def __init__(
        self,
        dir: str,
        type: BaseEnums.ServiceLoggerType,
        service_key: BaseTypes.OptionalString = None,
        level: BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO,
        google_cloud_logging: Optional[GoogleCloudLogging] = None
    ):
        super().__init__(
            dir=dir,
            type=type,
            service_key=service_key,
            middleware_type=None,
            client_key=None,
            level=level,
            google_cloud_logging=google_cloud_logging
        )

class ClientLogger(BaseLogger):
    def __init__(
        self,
        dir: str,
        client_key: str,
        service_key: BaseTypes.OptionalString = None,
        level: BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO,
        google_cloud_logging: Optional[GoogleCloudLogging] = None
    ):
        super().__init__(
            dir=dir,
            type=BaseEnums.LoggerType.CLIENT,
            service_key=service_key,
            middleware_type=None,
            client_key=client_key,
            level=level,
            google_cloud_logging=google_cloud_logging
        )