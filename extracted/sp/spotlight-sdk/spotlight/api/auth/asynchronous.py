"""
Asynchronous auth API requests.
"""

from typing import Optional

import aiohttp
from requests import Response

from spotlight.api.auth.__util import (
    _login_request_info,
    _refresh_token_request_info,
    _token_exchange_request_info,
)
from spotlight.core.common.function import build_response_obj


async def async_login(
    username: str, password: str, scope: Optional[str] = None
) -> Response:
    """
    Asynchronously login.

    Args:
        username (str): Username
        password (str): Password
        scope (Optional[str]): Token scope, such as 'offline_access'

    Returns:
        dict: Authentication/authorization response
    """
    request_info = _login_request_info(username, password, scope)
    async with aiohttp.ClientSession() as session:
        async with session.post(**request_info) as response:
            return await build_response_obj(response)


async def async_refresh_token(token: Optional[str]) -> Response:
    """
    Asynchronously refresh token. To get an offline access token, initial authentication (login) needs to use the scope
    'offline_access', then an offline token can be created using the refresh_token in the authentication response.
    [Stack overflow reference](https://stackoverflow.com/questions/69207734/keycloak-offline-access-token-with-refresh-token-grant-type).

    Args:
        token (str): Refresh token

    Returns:
        dict: Authentication/authorization response
    """
    request_info = _refresh_token_request_info(token)
    async with aiohttp.ClientSession() as session:
        async with session.post(**request_info) as response:
            return await build_response_obj(response)


async def async_exchange_token(requested_subject: str, subject_token: str) -> Response:
    """
    Asynchronously exchange token.

    Args:
        requested_subject (str): Request subject (Username or ID)
        subject_token (str): Token to swap

    Returns:
        dict: Authentication/authorization response
    """
    request_info = _token_exchange_request_info(requested_subject, subject_token)
    async with aiohttp.ClientSession() as session:
        async with session.post(**request_info) as response:
            return await build_response_obj(response)
