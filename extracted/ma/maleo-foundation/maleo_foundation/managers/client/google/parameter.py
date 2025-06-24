from google.api_core import retry
from google.api_core.exceptions import NotFound
from google.cloud import parametermanager
from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from .base import GoogleClientManager

class GoogleParameterManager(GoogleClientManager):
    def __init__(
        self,
        log_config: SimpleConfig,
        service_key: BaseTypes.OptionalString = None,
        credentials: Optional[Credentials] = None,
        credentials_path: Optional[Union[Path, str]] = None
    ) -> None:
        key = "google-parameter-manager"
        name = "GoogleParameterManager"
        super().__init__(
            key,
            name,
            log_config,
            service_key,
            credentials,
            credentials_path
        )
        self._client = parametermanager.ParameterManagerClient(credentials=self._credentials)
        self._logger.info("Client manager initialized successfully")

    @property
    def client(self) -> parametermanager.ParameterManagerClient:
        return self._client

    def dispose(self) -> None:
        if self._client is not None:
            self._logger.info("Disposing client manager")
            self._client = None
            self._logger.info("Client manager disposed successfully")