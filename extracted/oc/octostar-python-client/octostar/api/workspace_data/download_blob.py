from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from urllib.parse import quote
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    filename: str,
    *,
    client: Client = None,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/files/download-blob/{}".format(base_url, quote(filename, safe=""))

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["external_url"] = external_url

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    if response.status_code == HTTPStatus.OK:
        return response.json()
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": response.content,
        "headers": response.headers,
        "parsed": _parse_response(client=client, response=response),
    }
    return Response(**response_kwargs)


def sync_detailed(
    filename: str,
    *,
    client: Client = None,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Dict[str, Any]]:
    """## Request download from temp bucket

      Generate presigned URL for downloading a file from a temporary S3 bucket.
      Returns a presigned URL that allows direct download from the user's temporary bucket.

    ### Args:
    * `filename`: filename (str): Name of the file to download
    * `external_url`: external_url (Union[Unset, None, bool]): Whether to use the external endpoint URL
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Dict[str, Any]]` containing 'url' for presigned download
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        filename,
        client=client,
        external_url=external_url,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    if response.is_error:
        print(
            f"{str(response.status_code)} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    filename: str,
    *,
    client: Client = None,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Dict[str, Any]]:
    """## Request download from temp bucket

      Generate presigned URL for downloading a file from a temporary S3 bucket.
      Returns a presigned URL that allows direct download from the user's temporary bucket.

    ### Args:
    * `filename`: filename (str): Name of the file to download
    * `external_url`: external_url (Union[Unset, None, bool]): Whether to use the external endpoint URL
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Optional[Dict[str, Any]]` containing 'url' for presigned download
    """

    return sync_detailed(
        filename,
        client=client,
        external_url=external_url,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    filename: str,
    *,
    client: Client = None,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Dict[str, Any]]:
    """## Request download from temp bucket

      Generate presigned URL for downloading a file from a temporary S3 bucket.
      Returns a presigned URL that allows direct download from the user's temporary bucket.

    ### Args:
    * `filename`: filename (str): Name of the file to download
    * `external_url`: external_url (Union[Unset, None, bool]): Whether to use the external endpoint URL
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Dict[str, Any]]` containing 'url' for presigned download
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        filename,
        client=client,
        external_url=external_url,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    filename: str,
    *,
    client: Client = None,
    external_url: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Dict[str, Any]]:
    """## Request download from temp bucket

      Generate presigned URL for downloading a file from a temporary S3 bucket.
      Returns a presigned URL that allows direct download from the user's temporary bucket.

    ### Args:
    * `filename`: filename (str): Name of the file to download
    * `external_url`: external_url (Union[Unset, None, bool]): Whether to use the external endpoint URL
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Optional[Dict[str, Any]]` containing 'url' for presigned download
    """

    return (
        await asyncio_detailed(
            filename,
            client=client,
            external_url=external_url,
            accept=accept,
        )
    ).parsed
