import json
import os
from typing import Optional, Tuple

from requests.auth import AuthBase, HTTPBasicAuth

from qwak_inference.authentication._login_arguments import LoginArguments
from qwak_inference.authentication._utils import BearerAuth, EmptyAuth
from qwak_inference.authentication.constants import (
    CONFIG_FILE_PATH,
    FROG_ML_CONFIG_ACCESS_TOKEN,
    FROG_ML_CONFIG_ARTIFACTORY_URL,
    FROG_ML_CONFIG_PASSWORD,
    FROG_ML_CONFIG_USER,
    JF_ACCESS_TOKEN,
    JF_URL,
)
from qwak_inference.configuration.auth_config import AuthConfig
from qwak_inference.configuration.log_config import logger


def read_frogml_config() -> Optional[dict]:
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        logger.debug("FrogMl config file was not found.")
        return None
    except json.JSONDecodeError as e:
        logger.debug(f"FrogMl config file is not a valid JSON {e}.")
        return None


def __check_is_valid_frogml_auth_file(server_config: dict) -> bool:
    has_url: bool = FROG_ML_CONFIG_ARTIFACTORY_URL in server_config
    if not has_url:
        logger.debug(
            "Invalid FrogMl authentication file, expected either artifactory_url in FrogMl authentication file"
        )
        return False

    has_user: bool = FROG_ML_CONFIG_USER in server_config
    has_password: bool = FROG_ML_CONFIG_PASSWORD in server_config
    is_missing_user_or_password: bool = (has_user and not has_password) or (
        not has_user and has_password
    )

    if is_missing_user_or_password:
        logger.debug(
            "Invalid FrogMl authentication file, username or password is missing in FrogMl authentication file"
        )
        return False

    return True


def __get_login_arguments(server_config: dict) -> LoginArguments:
    login_args = LoginArguments()
    login_args.artifactory_url = server_config.get(FROG_ML_CONFIG_ARTIFACTORY_URL)

    has_access_token: bool = FROG_ML_CONFIG_ACCESS_TOKEN in server_config
    has_user: bool = FROG_ML_CONFIG_USER in server_config
    has_password: bool = FROG_ML_CONFIG_PASSWORD in server_config

    if has_access_token:
        login_args.access_token = server_config.get(FROG_ML_CONFIG_ACCESS_TOKEN)
    elif has_user and has_password:
        login_args.username = server_config.get(FROG_ML_CONFIG_USER)
        login_args.password = server_config.get(FROG_ML_CONFIG_PASSWORD)

    is_anonymous = (
        login_args.username is None
        and login_args.password is None
        and login_args.access_token is None
    )
    if is_anonymous:
        login_args.is_anonymous = True

    return login_args


def get_frogml_configuration() -> Optional[LoginArguments]:
    frog_ml_config: Optional[dict] = read_frogml_config()
    is_frogml_config_not_defined: bool = (
        not frog_ml_config
        or frog_ml_config.get("servers") is None
        or len(frog_ml_config["servers"]) <= 0
    )

    if is_frogml_config_not_defined:
        return None

    server_config: dict = frog_ml_config["servers"][0]
    is_valid_auth_file: bool = __check_is_valid_frogml_auth_file(server_config)

    if not is_valid_auth_file:
        return None

    login_args: LoginArguments = __get_login_arguments(server_config)

    return login_args


def get_credentials(auth_config: Optional[AuthConfig] = None) -> Tuple[str, AuthBase]:
    if not __should_use_file_auth(auth_config):
        __validate_credentials(auth_config)
        return __auth_config_to_auth_tuple(auth_config)
    logger.debug(
        "Login configuration not supplied, attempting to find environment variables"
    )

    if __should_use_environment_variables():
        return get_environment_variables()

    logger.debug(
        "Environment variables not supplied, attempting to load configuration from file"
    )

    if os.path.exists(CONFIG_FILE_PATH):
        return __read_credentials_from_file(CONFIG_FILE_PATH)
    raise ValueError(
        f"Configuration were not provided and configuration file not found in {CONFIG_FILE_PATH},"
        f" either pass configuration in the constructor, add env variables or create the configuration file by "
        f"running `frogml login`"
    )


def __should_use_environment_variables() -> bool:
    return os.getenv("JF_URL") is not None


def get_environment_variables() -> Tuple[str, AuthBase]:
    auth_config: AuthConfig = AuthConfig(
        artifactory_url=os.getenv(JF_URL),
        access_token=os.getenv(JF_ACCESS_TOKEN),
    )

    return __auth_config_to_auth_tuple(auth_config)


def __should_use_file_auth(credentials: Optional[AuthConfig] = None) -> bool:
    return credentials is None or (
        credentials.artifactory_url is None
        and credentials.user is None
        and credentials.password is None
        and credentials.access_token is None
    )


def __validate_credentials(credentials: Optional[AuthConfig]) -> None:
    if credentials is None:
        raise ValueError("Credentials must be provided.")
    if credentials.artifactory_url is None:
        raise ValueError("Credentials must contain artifactory url.")
    return None


def __read_credentials_from_file(file_path: str) -> Tuple[str, AuthBase]:
    try:
        with open(file_path, "r") as file:
            config_content: dict = json.load(file)
            servers = config_content.get("servers")
            if servers is None or len(servers) == 0:
                raise ValueError(
                    "Configuration file was found but it's empty, failing authentication"
                )
            server = servers[0]
            return __auth_config_to_auth_tuple(AuthConfig.from_dict(server))
    except json.JSONDecodeError:
        raise ValueError(f"Error when reading {file_path}, please recreate the file.")


def __auth_config_to_auth_tuple(
    auth_config: Optional[AuthConfig],
) -> Tuple[str, AuthBase]:
    if auth_config.artifactory_url is None:
        raise ValueError("No artifactory URL provided")

    auth: AuthBase = __get_auth_provider(auth_config)

    return auth_config.artifactory_url, auth


def __get_auth_provider(auth_config: Optional[AuthConfig]) -> AuthBase:
    auth: AuthBase = EmptyAuth()

    if auth_config is None:
        raise ValueError("No authentication configuration provided")

    if auth_config.access_token is not None:
        auth = BearerAuth(auth_config.access_token)
    elif auth_config.user is not None and auth_config.password is not None:
        auth = HTTPBasicAuth(auth_config.user, auth_config.password)
    elif auth_config.user is not None or auth_config.password is not None:
        raise ValueError("User and password must be provided together")

    return auth
