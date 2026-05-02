"""
Authorization decorators.
"""

import functools
from typing import Any, Callable, Optional

from aiocache.decorators import cached
from requests import Response

from spotlight.api.auth import async_login, async_refresh_token
from spotlight.core.common.config import EnvironmentConfig
from spotlight.core.common.decorators.authorization.__util import (
    _access_token,
    _handle_auth_response,
    _validate_headers,
)


def async_authenticated_request(
    request: Callable = None, *, env_config: Optional[EnvironmentConfig] = None
) -> Callable:
    """
    Decorator for requests that need to be authenticated

    Args:
          request (Callable): Method that needs auth headers injected
          env_config (Optional[EnvironmentConfig]): Optional environment config
    Returns:
        Callable: Wrapped function
    """

    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        async def wrap(*args, **kwargs) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                Any: The output of the wrapped function
            """
            config = env_config if env_config is not None else EnvironmentConfig()
            headers = kwargs.get("headers", {})

            if config.auth_config.can_authenticate():
                auth_headers = await _authenticate(
                    username=config.auth_config.username,
                    password=config.auth_config.password,
                    access_token=config.auth_config.access_token,
                    refresh_token=config.auth_config.refresh_token,
                )
                auth_headers.update(
                    headers
                )  # override authentication header if already provided
                kwargs["headers"] = auth_headers

            return await _make_request(f, config, *args, **kwargs)

        return wrap

    if request is None:
        return decorator
    return decorator(request)


@cached(ttl=1740)
async def _authenticate(
    username: Optional[str],
    password: Optional[str],
    access_token: Optional[str],
    refresh_token: Optional[str],
) -> dict:
    """
    Asynchronously authenticate user and create user authentication headers.

    Args:
        username (Optional[str]): Spotlight username
        password (Optional[str]): Spotlight password
        access_token (Optional[str]): Spotlight access token
        refresh_token (Optional[str]): Spotlight refresh token

    Returns:
        dict: Auth headers for a request
    """
    auth_headers = {}
    if username and password:
        auth_headers = await _sign_in(username=username, password=password)
    elif access_token:
        auth_headers = _access_token(access_token)
    elif refresh_token:
        auth_headers = await _refresh_token(refresh_token)
    return auth_headers


async def _sign_in(username: str, password: str) -> dict:
    auth_response = await async_login(username, password)
    return _handle_auth_response(auth_response, error_msg="Failed to sign-in the user")


async def _refresh_token(refresh_token: Optional[str] = None) -> dict:
    auth_response = await async_refresh_token(refresh_token)
    return _handle_auth_response(
        auth_response, error_msg="Failed to refresh the user's token"
    )


async def _make_request(func, config: EnvironmentConfig, *args, **kwargs) -> Response:
    _validate_headers(**kwargs)

    response: Response = await func(*args, **kwargs)
    if response.status_code == 401 and config.auth_config.refresh_token:
        auth_headers = await _refresh_token(config.auth_config.refresh_token)
        kwargs["headers"].update(auth_headers)  # override authentication header
        response: Response = await func(*args, **kwargs)

    return response
