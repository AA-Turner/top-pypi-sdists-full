import http
from typing import Optional

import requests
from requests.auth import AuthBase, HTTPBasicAuth

from frogml_storage.artifactory import ArtifactoryApi
from frogml_storage.logging import logger
from frogml_storage.authentication.models import BearerAuth, EmptyAuth
from frogml_storage.authentication.utils import (
    get_encrypted_password,
    save_auth_config,
)
from frogml_storage.authentication.models import AuthConfig
from frogml_storage.authentication.utils import (
    is_username_password_login,
    is_access_token_login,
    is_anonymous_login,
)


def run(auth_config: AuthConfig, anonymous: Optional[bool] = False) -> bool:
    if is_username_password_login(auth_config, anonymous):
        connection_validation_result = __login_by_username_password(auth_config)
    elif is_access_token_login(auth_config, anonymous):
        connection_validation_result = __validate_server_connection(
            auth_config, BearerAuth(auth_config.access_token)
        )
    elif is_anonymous_login(auth_config, anonymous):
        connection_validation_result = __validate_server_connection(
            auth_config, EmptyAuth()
        )
    else:
        connection_validation_result = False

    if connection_validation_result:
        save_auth_config(auth_config)
    return connection_validation_result


def __login_by_username_password(auth_config: AuthConfig) -> bool:
    if auth_config.user is not None and auth_config.password is not None:
        auth_token = HTTPBasicAuth(auth_config.user, auth_config.password)
        connection_validation_result = __validate_server_connection(
            auth_config, auth_token
        )
        if connection_validation_result:
            encrypted_password = get_encrypted_password(auth_config, auth_token)
            if encrypted_password is not None:
                auth_config.password = encrypted_password
                return True
    return False


def __validate_server_connection(auth_config: AuthConfig, auth_token: AuthBase) -> bool:
    success = False
    try:
        logger.debug("Attempting to ping artifactory")
        response = ArtifactoryApi(auth_config.artifactory_url, auth_token).ping()
        if response.status_code == http.HTTPStatus.OK:
            success = True
        else:
            logger.debug(
                f"Expected {http.HTTPStatus.OK} status but got {response.status_code} "
                f"when using url {auth_config.artifactory_url}"
            )
    except requests.exceptions.ConnectionError as e:
        logger.debug(f"Unable to connect to the provided url :{e}.")
    except requests.exceptions.MissingSchema as e:
        logger.debug(f"Invalid Artifactory URL provided: {e}.")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Unexpected request exception: {e}.")

    return success
