import logging
from time import time
from typing import Any, Optional, Union

from requests.exceptions import HTTPError

from dealcloud_sdk.constants.auth import AVAILABLE_SCOPES, AvailableScopeTypes
from dealcloud_sdk.constants.env_var_names import (
    CLIENT_ID_ENV_NAME,
    CLIENT_SECRET_ENV_NAME,
    SITE_URL_ENV_NAME,
)
from dealcloud_sdk.factories.from_env import dc_from_environment_variables
from dealcloud_sdk.factories.from_json import dc_from_json_config
from dealcloud_sdk.factories.from_yaml import dc_from_yaml_config
from dealcloud_sdk.models.auth import Tokens
from dealcloud_sdk.utils.get_key import get_key
from dealcloud_sdk.utils.request_retry import request_with_retry
from dealcloud_sdk.utils.validation import validate_scope


class DealCloudBase:
    """DealCloudBase provides the base definition for authentication, etc. to provide DealCloud python wrappers"""

    def __init__(
        self,
        site_url: str,
        client_id: Union[str, int],
        client_secret: str,
        scope: AvailableScopeTypes = AVAILABLE_SCOPES,
        refresh_id_maps: bool = True,
    ):
        """
        Init function for DealCloudBase

        Args:
            site_url(str): the target DealCloud site in the format "{client}.dealcloud.com" - i.e. no https:// or /
            client_id(int): the client id from the user api key
            client_secret(str): the client secret from the user api key
            scope(tuple[str]): the authentication scopes, defaults to ("data", "user_management", "publish")
        """
        # log with provided logger
        self._logger = logging.getLogger(__name__)

        # api credentials
        self._site = site_url
        self._client_id = client_id
        self._client_secret = client_secret

        # encode auth string for authentication using request header
        self._basic_auth = get_key(str(self._client_id), self._client_secret)

        # validate provided scopes against available scopes
        validate_scope(scope)
        self._scope = " ".join(scope)

        # id map refresh flag
        self._refresh_id_maps = refresh_id_maps

        # base urls
        self._url_root = f"https://{self._site}/api/rest/v4"
        self._url_root_v1 = f"https://{self._site}/api/rest/v1"

        # schema endpoint
        self._schema_url = f"{self._url_root}/schema"

        # data endpoints
        self._data_url = f"{self._url_root}/data"
        self._entrydata_url = f"{self._data_url}/entrydata"
        self._rows_url = f"{self._entrydata_url}/rows"
        self._query_url = f"{self._rows_url}/query"
        self._views_url = f"{self._data_url}/rows/view"

        # setup token storage
        self._access_token: str
        self._expiry_time: float

        # check valid credentials
        self._logger.debug("validating credentials")
        self._auth()
        self._logger.debug("credentials validated")

        # store schema
        self._site_schema = self.get_schema()
        # store users
        self._user_map = dict({u.email.lower(): u.id for u in self.get_users()})

        # id mapping store
        self._id_map: dict[Any, dict[Any, int]] = {}

    @classmethod
    def from_env(
        cls,
        site_url_env_name: str = SITE_URL_ENV_NAME,
        client_id_env_name: str = CLIENT_ID_ENV_NAME,
        client_secret_env_name: str = CLIENT_SECRET_ENV_NAME,
    ):
        config = dc_from_environment_variables(
            site_url_env_name,
            client_id_env_name,
            client_secret_env_name,
        )

        return cls(
            config.site_url,
            config.client_id,
            config.client_secret,
        )

    @classmethod
    def from_json(
        cls, json_file_path: str, json_path_to_credentials: Optional[str] = None
    ):
        config = dc_from_json_config(json_file_path, json_path_to_credentials)
        return cls(
            config.site_url,
            config.client_id,
            config.client_secret,
        )

    @classmethod
    def from_yaml(
        cls, yaml_file_path: str, yaml_path_to_credentials: Optional[str] = None
    ):
        config = dc_from_yaml_config(yaml_file_path, yaml_path_to_credentials)
        return cls(
            config.site_url,
            config.client_id,
            config.client_secret,
        )

    def _auth(self) -> Tokens:
        """
        Authenticate with the DealCloud API

        Returns:
            tokens (Tokens): Pydantic model containing auth tokens
        """
        url = f"{self._url_root_v1}/oauth/token"
        payload = f"grant_type=client_credentials&scope={self._scope}"

        response = request_with_retry(
            "POST",
            url,
            self._basic_auth,
            data=payload,
            status_force_list=[429],
            auth_type="Basic",
            max_retries=5,
            content_type="application/x-www-form-urlencoded",
        )

        if response.status_code != 200:
            self._logger.warning(response.text)
            raise HTTPError("Could not authenticate! - check credentials")
        tokens = Tokens(**response.json())

        self._access_token = tokens.access_token
        self._expiry_time = time() + (tokens.expires_in - 120)

        return tokens

    def _get_access_token(self) -> str:
        if time() > self._expiry_time:
            self._logger.warning("RE-AUTHENTICATING")
            self._auth()

        return self._access_token

    def get_schema(self):
        pass

    def get_users(self):
        pass
