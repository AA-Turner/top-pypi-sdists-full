from typing import Optional

from frogml_storage.authentication.models import AuthConfig


def login_input_checks(
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    anonymous: bool = False,
) -> bool:
    return (
        __is_user_name_password_command(url, username, password, token, anonymous)
        or __is_access_token_command(url, username, password, token, anonymous)
        or __is_anonymous_command(url, username, password, token, anonymous)
    )


def is_login_without_params(
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    token: Optional[str] = None,
    anonymous: bool = False,
) -> bool:
    return (
        all(params is None for params in [url, username, password, token])
        and not anonymous
    )


def is_username_password_login(
    auth_config: AuthConfig, anonymous: Optional[bool] = False
) -> bool:
    return __is_user_name_password_command(
        url=auth_config.artifactory_url,
        username=auth_config.user,
        password=auth_config.password,
        token=auth_config.access_token,
        anonymous=anonymous,
    )


def is_access_token_login(
    auth_config: AuthConfig, anonymous: Optional[bool] = False
) -> bool:
    if anonymous is None:
        anonymous = False
    return __is_access_token_command(
        url=auth_config.artifactory_url,
        username=auth_config.user,
        password=auth_config.password,
        token=auth_config.access_token,
        anonymous=anonymous,
    )


def is_anonymous_login(
    auth_config: AuthConfig, anonymous: Optional[bool] = False
) -> bool:
    if anonymous is None:
        anonymous = False
    return __is_anonymous_command(
        url=auth_config.artifactory_url,
        username=auth_config.user,
        password=auth_config.password,
        token=auth_config.access_token,
        anonymous=anonymous,
    )


def __is_anonymous_command(
    url: Optional[str],
    username: Optional[str],
    password: Optional[str],
    token: Optional[str],
    anonymous: bool,
) -> bool:
    return (
        anonymous
        and all(params is None for params in [username, password, token])
        and url is not None
    )


def __is_access_token_command(
    url: Optional[str],
    username: Optional[str],
    password: Optional[str],
    token: Optional[str],
    anonymous: bool,
) -> bool:
    if anonymous:
        return False
    return all(params is None for params in [username, password]) and all(
        params is not None for params in [url, token]
    )


def __is_user_name_password_command(
    url: Optional[str],
    username: Optional[str],
    password: Optional[str],
    token: Optional[str],
    anonymous: Optional[bool] = False,
) -> bool:
    return (
        not anonymous
        and url is not None
        and username is not None
        and password is not None
        and token is None
    )
