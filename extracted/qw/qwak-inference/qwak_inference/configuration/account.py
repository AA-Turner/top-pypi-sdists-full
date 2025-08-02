import configparser
import errno
import logging
import os
from typing import Type, Union

from qwak_inference.authentication.authentication_utils import (
    get_credentials,
    get_frogml_configuration,
)
from qwak_inference.configuration import Auth0Client, FrogMLAuthClient, Session
from qwak_inference.constants import QwakConstants
from qwak_inference.exceptions import QwakLoginException


class UserAccountConfiguration:
    API_KEY_FIELD = "api_key"

    def __init__(
        self,
        config_file=None,
        auth_file=None,
        auth_client: Union[Type[Auth0Client], Type[FrogMLAuthClient]] = None,
    ):
        if config_file:
            self._config_file = config_file
        else:
            self._config_file = QwakConstants.QWAK_CONFIG_FILE

        if auth_file:
            self._auth_file = auth_file
        else:
            self._auth_file = QwakConstants.QWAK_AUTHORIZATION_FILE

        self._config = configparser.ConfigParser()
        self._auth = configparser.ConfigParser()
        self._auth_client = auth_client
        self._environment = Session().get_environment()
        self._force_qwak_auth = os.getenv("FORCE_QWAK_AUTH", "False").lower() in (
            "true",
            "1",
            "t",
        )

        if not self._auth_client:
            # Determine auth client based on FrogML configuration
            try:
                if (
                    get_frogml_configuration() or os.getenv("JF_URL")
                ) and not self._force_qwak_auth:
                    self._auth_client = FrogMLAuthClient
                else:
                    logging.warning(
                        "Failed to initialize JFrog authentication. "
                        "Falling back to Qwak authentication. If you intended to use JFrog authentication, "
                        "please ensure the following environment variables are set: JF_URL and JF_ACCESS_TOKEN. "
                        "Alternatively, you can configure JFrog authentication using the Qwak CLI."
                    )
                    self._auth_client = Auth0Client
            except (ImportError, Exception):
                logging.warning(
                    "JFrog authentication failed, fallback to Auth0 authentication"
                )
                self._auth_client = Auth0Client

    def configure_user(self, api_key) -> None:
        """
        Write user account to the given config file in an ini format. Configuration will be written under the 'default'
        section
        :param user_account: user account properties to be written
        """
        if issubclass(self._auth_client, Auth0Client):
            self._auth.read(self._auth_file)
            self._auth.remove_section(self._environment)
            with self._safe_open(self._auth_file) as authfile:
                self._auth.write(authfile)

            self._auth_client(api_key=api_key, auth_file=self._auth_file).login()

            self._config.read(self._config_file)

            with self._safe_open(self._config_file) as configfile:
                self._config[self._environment] = {}
                self._config[self._environment][self.API_KEY_FIELD] = api_key
                self._config.write(configfile)
        elif issubclass(self._auth_client, FrogMLAuthClient):
            # Use FrogML's login flow
            _url, _ = get_credentials(None)

            if not _url:
                raise QwakLoginException("Failed to authenticate with JFrog")
            # Validate access token
            # TODO: Remove once we support reference token
            token = self._auth_client().get_token()
            if not token or len(token) <= 64:
                raise QwakLoginException(
                    "Authentication with JFrog failed: Only Access Tokens are supported. Please ensure you are using a valid Access Token."
                )

    @staticmethod
    def _mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    @staticmethod
    def _safe_open(path):
        UserAccountConfiguration._mkdir_p(os.path.dirname(path))
        return open(path, "w")

    def get_user_apikey(self) -> str:
        """
        Get persisted user account from config file
        :return:
        """
        try:
            api_key = os.environ.get("QWAK_API_KEY")
            if api_key:
                Session().set_environment(api_key)
                return api_key
            else:
                self._config.read(self._config_file)
                return self._config.get(
                    section=self._environment, option=self.API_KEY_FIELD
                )

        except FileNotFoundError:
            raise QwakLoginException(
                f"Could not read user configuration from {self._config_file}. "
                f"Please make sure one has been set using `qwak configure` command"
            )

        except configparser.NoSectionError:
            raise QwakLoginException(
                f"Could not read user configuration from {self._config_file}. "
                f"Please make sure one has been set using `qwak configure` command"
            )
