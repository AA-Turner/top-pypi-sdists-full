from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.managers.client.base import ClientManager
from maleo_foundation.utils.loaders.credential.google import GoogleCredentialsLoader
from maleo_foundation.utils.logging import SimpleConfig

class GoogleClientManager(ClientManager):
    def __init__(
        self,
        key: str,
        name: str,
        log_config: SimpleConfig,
        service_key: BaseTypes.OptionalString = None,
        credentials: Optional[Credentials] = None,
        credentials_path: Optional[Union[Path, str]] = None
    ) -> None:
        super().__init__(key, name, log_config, service_key)
        if (credentials is not None and credentials_path is not None) or (credentials is None and credentials_path is None):
            raise ValueError("Only either 'credentials' or 'credentials_path' can be passed as parameter")

        if credentials is not None:
            self._credentials = credentials
        else:
            self._credentials = GoogleCredentialsLoader.load(credentials_path)

        self._project_id = self._credentials.project_id

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @property
    def project_id(self) -> str:
        return self._project_id