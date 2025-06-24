from google.api_core import retry
from google.api_core.exceptions import NotFound
from google.cloud import secretmanager
from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from .base import GoogleClientManager

class GoogleSecretManager(GoogleClientManager):
    def __init__(
        self,
        log_config: SimpleConfig,
        service_key: BaseTypes.OptionalString = None,
        credentials: Optional[Credentials] = None,
        credentials_path: Optional[Union[Path, str]] = None
    ) -> None:
        key = "google-secret-manager"
        name = "GoogleSecretManager"
        super().__init__(
            key,
            name,
            log_config,
            service_key,
            credentials,
            credentials_path
        )
        self._client = secretmanager.SecretManagerServiceClient(credentials=self._credentials)
        self._logger.info("Client manager initialized successfully")

    @property
    def client(self) -> secretmanager.SecretManagerServiceClient:
        return self._client

    def dispose(self) -> None:
        if self._client is not None:
            self._logger.info("Disposing client manager")
            self._client = None
            self._logger.info("Client manager disposed successfully")

    @retry.Retry(predicate=retry.if_exception_type(Exception), timeout=5)
    def get(
        self,
        name: str,
        version: str = "latest"
    ) -> str:
        #* Check if secret exists
        secret_name = f"projects/{self._project_id}/secrets/{name}"
        try:
            request = secretmanager.GetSecretRequest(name=secret_name)
            self._client.get_secret(request=request)
        except NotFound:
            self._logger.error("Secret '%s' did not exist", name, exc_info=True)
            raise
        except Exception:
            self._logger.error("Exception raised while checking secret '%s' existence", name, exc_info=True)
            raise

        #* Check if secret's version exists
        secret_version_name = f"{secret_name}/versions/{version}"
        try:
            request = secretmanager.GetSecretVersionRequest(name=secret_version_name)
            self._client.get_secret_version(request=request)
        except NotFound:
            self._logger.error("Secret '%s' with version '%s' did not exist", name, version, exc_info=True)
            raise
        except Exception:
            self._logger.error("Exception raised while checking secret '%s' with version '%s' existence", name, version, exc_info=True)
            raise

        #* Access secret's version
        try:
            request = secretmanager.AccessSecretVersionRequest(name=secret_version_name)
            response = self._client.access_secret_version(request=request)
            self._logger.info("Successfully retrieved secret '%s' with version '%s'", name, version)
            return response.payload.data.decode()
        except Exception:
            self._logger.error("Exception occured while retrieving secret '%s' with version '%s'", name, version, exc_info=True)
            raise

    @retry.Retry(predicate=retry.if_exception_type(Exception), timeout=5)
    def create(
        self,
        name: str,
        data: str
    ) -> str:
        parent = f"projects/{self._project_id}"
        secret_path = f"{parent}/secrets/{name}"
        try:
            #* Check if the secret already exists
            request = secretmanager.GetSecretRequest(name=secret_path)
            self._client.get_secret(request=request)
        except NotFound:
            #* Secret does not exist, create it first
            try:
                secret = secretmanager.Secret(name=name, replication={"automatic": {}})
                request = secretmanager.CreateSecretRequest(parent=parent, secret_id=name, secret=secret)
                self._client.create_secret(request=request)
            except Exception:
                self._logger.error("Exception occured while creating secret '%s'", name)
                raise

        #* Add a new secret version
        try:
            payload = secretmanager.SecretPayload(data=data.encode())
            request = secretmanager.AddSecretVersionRequest(parent=secret_path, payload=payload)
            response = self._client.add_secret_version(request=request)
            return data
        except Exception:
            self._logger.error("Exception occured while adding secret '%s' version", name)
            raise