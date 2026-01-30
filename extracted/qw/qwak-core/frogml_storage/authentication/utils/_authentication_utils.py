import http
import json
import os
from typing import Optional

import requests
from requests.auth import AuthBase, HTTPBasicAuth

from frogml_storage.artifactory import ArtifactoryApi
from frogml_storage.authentication.models import (
    BearerAuth,
    EmptyAuth,
    AuthConfig,
    LoginArguments,
)
from frogml_storage.constants import (
    CONFIG_FILE_PATH,
    FROG_ML_CONFIG_ACCESS_TOKEN,
    FROG_ML_CONFIG_ARTIFACTORY_URL,
    FROG_ML_CONFIG_PASSWORD,
    FROG_ML_CONFIG_USER,
    JF_ACCESS_TOKEN,
    JF_URL,
    SERVER_ID,
    JFROG_CLI_CONFIG_FILE_PATH,
    JFROG_CLI_CONFIG_ARTIFACTORY_URL,
    JFROG_CLI_CONFIG_URL,
    JFROG_CLI_CONFIG_ACCESS_TOKEN,
    JFROG_CLI_CONFIG_USER,
    JFROG_CLI_CONFIG_PASSWORD,
)
from frogml_storage.logging import logger
from frogml_storage.utils import join_url


def read_jfrog_cli_config() -> Optional[dict]:
    try:
        with open(JFROG_CLI_CONFIG_FILE_PATH, "r") as file:
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        logger.debug("JFrog cli config file was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"JFrog cli config file is not a valid JSON {e}.")
        return None


def read_frogml_config() -> Optional[dict]:
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        logger.debug("FrogMl config file was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"FrogMl config file is not a valid JSON {e}.")
        return None


def parse_cli_config_server(server_config: dict) -> Optional[LoginArguments]:
    login_args = LoginArguments()
    login_args.server_id = server_config.get(SERVER_ID)

    if JFROG_CLI_CONFIG_ARTIFACTORY_URL in server_config:
        login_args.artifactory_url = server_config.get(JFROG_CLI_CONFIG_ARTIFACTORY_URL)
    elif (
        JFROG_CLI_CONFIG_URL in server_config
        and server_config.get(JFROG_CLI_CONFIG_URL) is not None
    ):
        login_args.artifactory_url = join_url(
            server_config[JFROG_CLI_CONFIG_URL], "artifactory"
        )
    else:
        logger.debug(
            "Invalid JFrog CLI file, expected either artifactoryUrl or url in jfrog cli config file"
        )
        return None

    if JFROG_CLI_CONFIG_ACCESS_TOKEN in server_config:
        login_args.access_token = server_config.get(JFROG_CLI_CONFIG_ACCESS_TOKEN)
    elif (
        JFROG_CLI_CONFIG_USER in server_config
        and JFROG_CLI_CONFIG_PASSWORD in server_config
    ):
        login_args.username = server_config.get(JFROG_CLI_CONFIG_USER)
        login_args.password = server_config.get(JFROG_CLI_CONFIG_PASSWORD)
    else:
        logger.debug(
            "Expected either accessToken or user/password in jfrog cli config file"
        )
        return None

    return login_args


def get_frogml_configuration() -> Optional[LoginArguments]:
    frog_ml_config = read_frogml_config()
    if (
        frog_ml_config is not None
        and frog_ml_config.get("servers") is not None
        and len(frog_ml_config["servers"]) > 0
    ):
        server_config = frog_ml_config["servers"][0]
        login_args = LoginArguments()
        if FROG_ML_CONFIG_ARTIFACTORY_URL in server_config:
            login_args.artifactory_url = server_config.get(
                FROG_ML_CONFIG_ARTIFACTORY_URL
            )
        else:
            logger.debug(
                "Invalid FrogMl authentication file, expected either artifactory_url in FrogMl authentication file"
            )
            return None

        if FROG_ML_CONFIG_ACCESS_TOKEN in server_config:
            login_args.access_token = server_config.get(FROG_ML_CONFIG_ACCESS_TOKEN)
        elif (
            FROG_ML_CONFIG_USER in server_config
            and FROG_ML_CONFIG_PASSWORD in server_config
        ):
            login_args.username = server_config.get(FROG_ML_CONFIG_USER)
            login_args.password = server_config.get(FROG_ML_CONFIG_PASSWORD)
        elif (
            FROG_ML_CONFIG_USER in server_config
            and FROG_ML_CONFIG_PASSWORD not in server_config
            or (
                FROG_ML_CONFIG_USER not in server_config
                and FROG_ML_CONFIG_PASSWORD in server_config
            )
        ):
            logger.debug(
                "Invalid FrogMl authentication file, username or password is missing in FrogMl authentication file"
            )
            return None
        elif (
            login_args.username is None
            and login_args.password is None
            and login_args.access_token is None
        ):
            login_args.isAnonymous = True
        return login_args
    else:
        return None


def get_credentials(auth_config: Optional[AuthConfig] = None) -> tuple[str, AuthBase]:
    if not __should_use_file_auth(auth_config):
        __validate_credentials(auth_config)
        return __auth_config_to_auth_tuple(auth_config)
    logger.debug(
        "Login configuration not supplied, attempting to find environment variables"
    )

    if __should_use_environment_variables():
        return __get_environment_variables()

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


def get_encrypted_password(
    auth_config: AuthConfig, auth_token: AuthBase
) -> Optional[str]:
    try:
        response = ArtifactoryApi(
            auth_config.artifactory_url, auth_token
        ).encrypt_password()
        if response.status_code != http.HTTPStatus.OK:
            logger.debug(
                f"Expected {http.HTTPStatus.OK} status but got {response.status_code} "
                f"when using url {auth_config.artifactory_url}"
            )
            print("Error while trying to encrypt password.")
            return None
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error while trying to encrypt password: {e}.")
        return None


def save_auth_config(auth_config: AuthConfig) -> None:
    file_content: dict[str, list] = {}
    file_content.setdefault("servers", []).append(auth_config.to_json())
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)

    with open(CONFIG_FILE_PATH, "w") as file:
        json.dump(file_content, file, indent=2)


def get_list_of_servers_from_config(jfrog_cli_config: dict) -> list[str]:
    if jfrog_cli_config is not None:
        servers = jfrog_cli_config.get("servers")
        if servers is not None:
            return list(map(__map_server_ids, servers))

    return []


def __map_server_ids(server: dict) -> str:
    server_id = ""
    if server is not None:
        server_id = str(server.get("serverId"))

        if server.get("isDefault") is not None and bool(server.get("isDefault")):
            server_id = f"{server_id} (Default)"

    return server_id


def __should_use_environment_variables() -> bool:
    return os.getenv("JF_URL") is not None


def __get_environment_variables() -> tuple[str, AuthBase]:
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


def __read_credentials_from_file(file_path: str) -> tuple[str, AuthBase]:
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
) -> tuple[str, AuthBase]:

    if auth_config is None:
        raise ValueError("No authentication configuration provided")

    auth: AuthBase = EmptyAuth()
    if auth_config.access_token is not None:
        auth = BearerAuth(auth_config.access_token)
    elif auth_config.user is not None and auth_config.password is not None:
        auth = HTTPBasicAuth(auth_config.user, auth_config.password)
    elif auth_config.user is not None or auth_config.password is not None:
        raise ValueError("User and password must be provided together")

    if auth_config.artifactory_url is None:
        raise ValueError("No artifactory URL provided")

    return auth_config.artifactory_url, auth
