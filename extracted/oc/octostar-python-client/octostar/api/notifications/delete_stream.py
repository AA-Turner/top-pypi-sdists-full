from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.acknowledgement import Acknowledgement
from ...models.delete_stream_response_401 import DeleteStreamResponse401

from typing import cast


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    stream_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/streams/{stream_id}".format(base_url, stream_id=stream_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    if response.status_code == HTTPStatus.OK:
        response_200 = Acknowledgement.from_dict(response.json())
        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DeleteStreamResponse401.from_dict(response.json())
        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
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
    stream_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
    """## Delete a stream

      Delete a stream identified by its stream_id.

    ### Args:
    * `stream_id`: stream_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, Any, DeleteStreamResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        stream_id=stream_id,
        client=client,
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
    stream_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
    """## Delete a stream

      Delete a stream identified by its stream_id.

    ### Args:
    * `stream_id`: stream_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, Any, DeleteStreamResponse401]`
    """

    return sync_detailed(
        stream_id=stream_id,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    stream_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
    """## Delete a stream

      Delete a stream identified by its stream_id.

    ### Args:
    * `stream_id`: stream_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, Any, DeleteStreamResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
    kwargs = _get_kwargs(
        stream_id=stream_id,
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    stream_id: str,
    *,
    client: Client = None,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Acknowledgement, Any, DeleteStreamResponse401]]:
    """## Delete a stream

      Delete a stream identified by its stream_id.

    ### Args:
    * `stream_id`: stream_id (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, Any, DeleteStreamResponse401]`
    """

    return (
        await asyncio_detailed(
            stream_id=stream_id,
            client=client,
            accept=accept,
        )
    ).parsed
