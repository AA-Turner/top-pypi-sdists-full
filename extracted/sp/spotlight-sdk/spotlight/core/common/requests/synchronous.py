from typing import Optional

import requests
from requests import Response

from spotlight.core.common.config import EnvironmentConfig
from spotlight.core.common.decorators import authenticated_request

config = EnvironmentConfig()


@authenticated_request
def __get_request(
    endpoint: str,
    url_key: str = "spotlight",
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for get requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.get(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout,
    )


@authenticated_request
def __put_request(
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
    Wrapper method for put requests.

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
    return requests.put(
        url=f"{config.get_url(url_key)}/{endpoint}",
        data=data,
        json=json,
        files=files,
        headers=headers or {},
        params=params,
        timeout=timeout,
    )


@authenticated_request
def __post_request(
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
    Wrapper method for post requests.

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
    return requests.post(
        url=f"{config.get_url(url_key)}/{endpoint}",
        files=files,
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout,
    )


@authenticated_request
def __delete_request(
    endpoint: str,
    url_key: str = "spotlight",
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = 120,
) -> Response:
    """
    Wrapper method for delete requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.delete(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout,
    )
