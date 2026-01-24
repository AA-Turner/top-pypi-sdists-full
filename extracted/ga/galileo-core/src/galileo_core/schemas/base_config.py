# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
from logging import WARNING, _nameToLevel
from pathlib import Path
from ssl import SSLContext
from time import time
from typing import Any, Optional, Tuple, Type, TypeVar, Union

from jwt import decode as jwt_decode
from pydantic import Field, SecretStr, ValidationInfo, field_serializer, field_validator, model_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.api_client import ApiClient
from galileo_core.helpers.execution import async_run
from galileo_core.helpers.logger import logger
from galileo_core.helpers.ssl_context import get_ssl_context
from galileo_core.schemas.core.user import User

AGalileoConfig = TypeVar("AGalileoConfig", bound="GalileoConfig")


class GalileoConfig(BaseSettings):
    log_level: int = Field(default=WARNING, validate_default=True)
    ssl_context: Union[SSLContext, bool] = Field(
        default=True, validate_default=True, exclude=True, description="SSL context for the API client."
    )
    home_dir: Path = Field(
        default=Path().home().joinpath(".galileo"),
        validate_default=True,
        description="Home directory for Galileo.",
        exclude=True,
    )

    console_url: Url
    api_url: Optional[Url] = None

    # User auth details.
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    api_key: Optional[SecretStr] = None
    sso_id_token: Optional[SecretStr] = None
    sso_provider: Optional[str] = None

    jwt_token: Optional[SecretStr] = None
    refresh_token: Optional[SecretStr] = None
    current_user: Optional[str] = None

    # Validated API client. This is set as a part of the initialization.
    # We set the API URL and JWT token on the API client and make a request to
    # confirm that the user is logged in successfully.
    # This is set as an exclude field to avoid serializing it to the config file.
    validated_api_client: Optional[ApiClient] = Field(
        default=None,
        validate_default=True,
        exclude=True,
        description="Validated API client that is with the user's JWT token after a successful login.",
    )

    # Config file for this project.
    config_filename: str = "galileo-config.json"

    model_config = SettingsConfigDict(
        # Allow loading from environment variables.
        env_prefix="GALILEO_",
        # Allow unknown fields when loading from a config file.
        extra="allow",
    )

    @field_validator("ssl_context", mode="before")
    def set_ssl_context(cls, value: Union[SSLContext, bool]) -> Union[SSLContext, bool]:
        return get_ssl_context(value)

    @field_validator("home_dir", mode="before")
    def set_home_dir(cls, value: Union[str, Path]) -> Path:
        """
        Set the home directory for the config file.

        Parameters
        ----------
        value : Optional[Path]
            Home directory to set.

        Returns
        -------
        Path
            Home directory to use.
        """
        value = Path(value)
        if not value.exists():
            value.mkdir(parents=True, exist_ok=True)
        if not value.is_dir():
            raise ValueError(f"`GALILEO_HOME_DIR` {value} is not a directory.")
        return value

    @property
    def config_file(self) -> Path:
        return self.home_dir.joinpath(self.config_filename)

    @field_validator("log_level", mode="before")
    def set_log_level(cls, value: Optional[Union[int, str]]) -> int:
        """
        Set the log level for the logger.

        We allow setting the log level using the string representation of the log level
        or the integer representation of the log level.

        By default, we set the log level to `WARNING`.

        Parameters
        ----------
        value : Optional[Union[int, str]]
            Log level to set.

        Returns
        -------
        int
            Log level set.
        """
        if isinstance(value, str):
            value = value.upper()
            log_level = _nameToLevel.get(value, WARNING)
        elif isinstance(value, int):
            log_level = value
        else:
            log_level = WARNING
        logger.setLevel(log_level)
        return log_level

    @field_validator("console_url", mode="before")
    def ensure_https_console_url(cls, value: str) -> str:
        """
        Ensure that the console URL is an HTTPS URL.

        Parameters
        ----------
        value : str
            Console URL to validate.

        Returns
        -------
        str
            Validated console URL.
        """
        if value and not (value.startswith("https") or value.startswith("http")):
            value = f"https://{value}"
        return value

    @field_validator("api_url", mode="before")
    def set_api_url(cls, api_url: Optional[Union[str, Url]], info: ValidationInfo) -> Url:
        """
        Set the API URL if it's not already set.

        We can set the API URL in the following ways:
        1. If the API URL is provided, use it.
        2. If the console URL matches `localhost` or `127.0.0.1`, use `http://localhost:8088`.
        3. If the API URL is not provided, use the console URL to generate the API URL
        by replacing `console` with `api`.

        Once we determine the API URL, we make a request to the healthcheck endpoint to
        validate that it is reachable.

        Parameters
        ----------
        api_url : Optional[Union[str, Url]]
            API URL to use. If not provided, we generate it from the console URL.
        info : ValidationInfo
            Pydantic validation info object.

        Returns
        -------
        Url
            API URL to use.

        Raises
        ------
        ValueError
            If the console URL is not set.
        ValueError
            If the API URL can't be generated.
        """
        if api_url is None:
            console_url = info.data.get("console_url")
            if console_url is None:
                raise ValueError(
                    "Console URL is required. Please set the environment variable "
                    "`GALILEO_CONSOLE_URL` to your Galileo console URL."
                )
            else:
                console_url = console_url.unicode_string() if isinstance(console_url, Url) else console_url
            # Local dev.
            if any(["localhost" in console_url, "127.0.0.1" in console_url]):
                api_url = "http://localhost:8088"
            elif "app.galileo.ai" in console_url:
                api_url = "https://api.galileo.ai"
            else:
                api_url = console_url.replace("console", "api")
        if api_url is None:
            raise ValueError("API URL is required.")
        else:
            async_run(
                ApiClient.make_request(
                    RequestMethod.GET,
                    base_url=str(api_url),
                    endpoint=Routes.healthcheck,
                    ssl_context=info.data.get("ssl_context", True),
                )
            )
        return Url(api_url) if isinstance(api_url, str) else api_url

    @staticmethod
    def get_jwt_token(
        console_url: Optional[Url] = None,
        api_url: Optional[Url] = None,
        api_key: Optional[SecretStr] = None,
        username: Optional[str] = None,
        password: Optional[SecretStr] = None,
        sso_id_token: Optional[SecretStr] = None,
        sso_provider: Optional[str] = None,
        refresh_token: Optional[SecretStr] = None,
        ssl_context: Union[SSLContext, bool] = True,
    ) -> Tuple[SecretStr, Optional[SecretStr]]:
        """
        Get the JWT token for the user.

        1. If an API key is provided, log in with the API key.
        2. If a username and password are provided, log in with the username and password.
        3. If no credentials are provided, attempt to log in with a token from the UI.

        Parameters
        ----------
        console_url : Optional[HttpUrl], optional
            Console URL, by default None
        api_url : Optional[HttpUrl], optional
            API URL, by default None
        api_key : Optional[SecretStr], optional
            API key, by default None
        username : Optional[str], optional
            Username, by default None
        password : Optional[SecretStr], optional
            Password, by default None
        sso_id_token : Optional[SecretStr], optional
            SSO ID token, by default None
        sso_provider : Optional[str], optional
            SSO provider, by default None
        refresh_token : Optional[SecretStr], optional
            Refresh token, by default None
        ssl_context : Union[SSLContext, bool], optional
            SSL context, by default True

        Returns
        -------
        SecretStr
            JWT token for the user, if successful, as a secret string.

        Raises
        ------
        AssertionError
            If the console URL is not provided.
        AssertionError
            If the API URL is not provided.
        """

        token_data = dict()
        refresh_token_data: Optional[str] = None
        assert console_url is not None, "Console URL is required."
        assert api_url is not None, "API URL is required."

        if refresh_token:
            try:
                raw_response = async_run(
                    ApiClient.make_request(
                        RequestMethod.POST,
                        base_url=api_url.unicode_string(),
                        endpoint=Routes.refresh_token,
                        cookies={"refresh_token": refresh_token.get_secret_value()},
                        return_raw_response=True,
                    )
                )
                token_data = raw_response.json()
                refresh_token_data = raw_response.cookies.get("refresh_token")
                logger.debug("Token refreshed using refresh_token.")
            except Exception as e:
                logger.debug(f"Refreshing auth token with refresh failed: {e}.")
        if not token_data:
            if api_key:
                logger.debug("Logging in with API key.")
                token_data = async_run(
                    ApiClient.make_request(
                        RequestMethod.POST,
                        base_url=api_url.unicode_string(),
                        endpoint=Routes.api_key_login,
                        json=dict(api_key=api_key.get_secret_value()),
                        ssl_context=ssl_context,
                    )
                )
                logger.debug("Logged in with API key.")
            elif username and password:
                logger.debug("Logging in with username and password.")
                raw_response = async_run(
                    ApiClient.make_request(
                        RequestMethod.POST,
                        base_url=api_url.unicode_string(),
                        endpoint=Routes.username_login,
                        data=dict(
                            username=username,
                            password=password.get_secret_value(),
                            auth_method="email",
                        ),
                        ssl_context=ssl_context,
                        return_raw_response=True,
                    )
                )
                token_data = raw_response.json()
                refresh_token_data = raw_response.cookies.get("refresh_token")
                logger.debug("Logged in with username and password.")
            elif sso_id_token and sso_provider:
                logger.debug("Logging in with SSO ID token.")
                raw_response = async_run(
                    ApiClient.make_request(
                        RequestMethod.POST,
                        base_url=api_url.unicode_string(),
                        endpoint=Routes.social_login,
                        json=dict(id_token=sso_id_token.get_secret_value(), provider=sso_provider),
                        ssl_context=ssl_context,
                        return_raw_response=True,
                    )
                )
                token_data = raw_response.json()
                refresh_token_data = raw_response.cookies.get("refresh_token")
                logger.debug("Logged in with SSO ID token.")
        if (jwt_token := token_data.get("access_token", "")) == "":
            logger.debug("No credentials found.")
        else:
            logger.debug("JWT token received and set.")
        return SecretStr(jwt_token), SecretStr(refresh_token_data) if refresh_token_data else None

    @model_validator(mode="after")
    def set_jwt_token(self) -> "GalileoConfig":
        """
        Populate jwt_token and refresh_token if missing.

        Attempts authentication using available credentials and updates the tokens.
        Raises ValueError if jwt_token could not be obtained.

        Returns
        -------
        GalileoConfig
            The updated config instance with a validated API client.
        """
        if self.jwt_token is None:
            jwt_token, new_refresh_token = self.get_jwt_token(
                self.console_url,
                self.api_url,
                self.api_key,
                self.username,
                self.password,
                self.sso_id_token,
                self.sso_provider,
                self.refresh_token,
                self.ssl_context,
            )
            if jwt_token is None:
                raise ValueError("JWT token is required.")
            self.jwt_token = jwt_token
            if new_refresh_token:
                self.refresh_token = new_refresh_token

        return self

    @model_validator(mode="after")
    def set_validated_api_client(self) -> "GalileoConfig":
        """
        Set the validated API client.

        This method sets an API client with the validated API URL and JWT token. As a
        part of the validation process, we make a request to get the current user's email
        address to confirm that the user is logged in successfully.

        Returns
        -------
        GalileoConfig
            The updated config instance with a validated API client.
        """
        if self.api_url is None:
            raise ValueError("API URL is required.")
        if self.jwt_token is None:
            raise ValueError("JWT token is required.")
        self.validated_api_client = ApiClient(host=self.api_url, jwt_token=self.jwt_token, ssl_context=self.ssl_context)
        # Get the current user to confirm that the user is logged in successfully.
        current_user_dict = self.validated_api_client.request(RequestMethod.GET, path=Routes.current_user)
        _ = User.model_validate(current_user_dict)
        logger.debug("Logged in successfully.")
        return self

    @field_serializer("password", "jwt_token", "api_key", "sso_id_token", when_used="json-unless-none")
    def serialize_secrets(self, value: SecretStr) -> str:
        """Serialize secret strings to their secret values."""
        return value.get_secret_value()

    def write(self) -> None:
        """
        Write the config object to a file.

        This is only used as a backup for debugging and never read from to set current values.
        """
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(self.model_dump_json(exclude_none=True))

    def refresh_jwt_token(self) -> None:
        """Refresh token if not present or expired."""
        # Check to see if our token is expired or (will expire in the next 5 minutes) before making a request and
        # refresh token if it's expired.
        if self.jwt_token:
            claims = jwt_decode(self.jwt_token.get_secret_value(), options={"verify_signature": False})
            if claims.get("exp", 0) <= (time() + 300):
                logger.debug("JWT token is invalid, refreshing.")
                self.jwt_token, self.refresh_token = self.get_jwt_token(
                    self.console_url,
                    self.api_url,
                    self.api_key,
                    self.username,
                    self.password,
                    self.sso_id_token,
                    self.sso_provider,
                    self.refresh_token,
                )
            else:
                logger.debug("JWT token is still valid, not refreshing.")
        # If no token is present, log in.
        else:
            logger.debug("JWT token not found, getting a new one.")
            self.jwt_token, self.refresh_token = self.get_jwt_token(
                self.console_url,
                self.api_url,
                self.api_key,
                self.username,
                self.password,
                self.sso_id_token,
                self.sso_provider,
                self.refresh_token,
            )

    @property
    def api_client(self) -> ApiClient:
        """
        Get the API client.

        We refresh the JWT token if it's expired and set the JWT token on the API client
        if it's different from the one set on the API client during the config
        initialization.

        Returns
        -------
        ApiClient
            Validated API client.
        """
        assert self.validated_api_client is not None, "API client must be set before accessing it."
        self.refresh_jwt_token()
        if self.jwt_token and self.validated_api_client.jwt_token != self.jwt_token:
            self.validated_api_client.jwt_token = self.jwt_token
        return self.validated_api_client

    @classmethod
    def _get(cls: Type[AGalileoConfig], existing_config: Optional[AGalileoConfig], **kwargs: Any) -> "AGalileoConfig":
        """
        Internal method to get the config object.

        This method is used to set the config object from the global variable (passed in as an arg) or from the kwargs
        or environment variables. We use this so that we can maintain independent global variables for different
        sub-classes of the BaseConfig class in their respective modules, while still keeping the interaction predictable
        and consistent.
        """
        if kwargs:
            logger.debug("Setting config from arguments and environment variables.")
            return cls(**kwargs)
        elif existing_config is None:
            logger.debug("Setting config from environment variables.")
            return cls()
        else:
            # Ignore the type here because we know that _config is not None and is an object of the
            # GalileoConfig class or its sub-classes.
            logger.debug("Config is already set.")
            return existing_config  # type: ignore[return-value]

    @classmethod
    def get(cls: Type[AGalileoConfig], **kwargs: Any) -> "AGalileoConfig":
        """
        Get the config object from the global variable or set it if it's not already set from the kwargs or environment
        variables.

        This method should be implemented in the sub-classes to set the config object for the sub-class.
        """
        global _config
        # Ignore the type here because we know that _config is an object of the BaseConfig class or its sub-classes.
        _config = cls._get(_config, **kwargs)  # type: ignore[arg-type]
        return _config

    def reset(self) -> None:
        """
        Reset the credentials stored in the config object.

        Sub-classes can extend this method to reset additional fields.
        """
        self.username = None
        self.password = None
        self.api_key = None
        self.sso_id_token = None
        self.sso_provider = None

        self.jwt_token = None
        self.current_user = None
        self.validated_api_client = None

        global _config
        _config = None

        self.write()

    def logout(self) -> None:
        """Logout the user by resetting the credentials"""
        self.reset()


# Global config object that is used to store the config object after the first load.
_config: Optional[GalileoConfig] = None
