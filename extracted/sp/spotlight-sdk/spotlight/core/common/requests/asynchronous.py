from typing import Optional

import aiohttp
from requests import Response

from spotlight.core.common.config import EnvironmentConfig
from spotlight.core.common.decorators import async_authenticated_request
from spotlight.core.common.function import build_response_obj

config = EnvironmentConfig()


@async_authenticated_request
async def __async_get_request(
    endpoint: str,
    url_key: str = "spotlight",
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for asynchronous get requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"{config.get_url(url_key)}/{endpoint}",
            headers=headers or {},
            params=params,
            timeout=timeout,
        ) as response:
            result = await build_response_obj(response)

    return result


@async_authenticated_request
async def __async_put_request(
    endpoint: str,
    url_key: str = "spotlight",
    data=None,
    json=None,
    files=None,
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for asynchronous put requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    if files:
        data = files

    async with aiohttp.ClientSession() as session:
        async with session.put(
            url=f"{config.get_url(url_key)}/{endpoint}",
            data=data,
            json=json,
            headers=headers or {},
            params=params,
            timeout=timeout,
        ) as response:
            result = await build_response_obj(response)

    return result


@async_authenticated_request
async def __async_post_request(
    endpoint: str,
    url_key: str = "spotlight",
    files=None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for asynchronous post requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    if files:
        data = files

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{config.get_url(url_key)}/{endpoint}",
            data=data,
            json=json,
            headers=headers or {},
            params=params,
            timeout=timeout,
        ) as response:
            result = await build_response_obj(response)

    return result


@async_authenticated_request
async def __async_delete_request(
    endpoint: str,
    url_key: str = "spotlight",
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for asynchronous delete requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            url=f"{config.get_url(url_key)}/{endpoint}",
            headers=headers or {},
            params=params,
            timeout=timeout,
        ) as response:
            result = await build_response_obj(response)

    return result
