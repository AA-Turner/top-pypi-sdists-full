from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from typing import cast, List
from typing import Union
from typing import cast
from typing import Optional
from ...models.octostar_event import OctostarEvent
from ...models.pull_events_from_stream_response_401 import (
    PullEventsFromStreamResponse401,
)
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    stream_id: str,
    *,
    client: Client = None,
    count: Union[Unset, None, int] = 10,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/streams/{stream_id}".format(base_url, stream_id=stream_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["count"] = count

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
) -> Optional[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_json = response.json()
        # New FastAPI endpoint wraps events in {"events": [...], "count": N}
        _response_200 = (
            _response_json.get("events", _response_json)
            if isinstance(_response_json, dict)
            else _response_json
        )
        for response_200_item_data in _response_200:
            response_200_item = OctostarEvent.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = PullEventsFromStreamResponse401.from_dict(response.json())

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
) -> Response[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": response.content,
        "headers": response.headers,
        "parsed": _parse_response(client=client, response=response),
    }
    return Response(**response_kwargs)


def _build_chunk_response(
    *, client: Client = None, response: httpx.Response, chunk: bytes
) -> Response[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": chunk,
        "headers": response.headers,
        "parsed": None,  # cannot parse incomplete chunks of data, we leave it to the user
    }
    return Response(**response_kwargs)


def sync_detailed(
    stream_id: str,
    *,
    client: Client = None,
    count: Union[Unset, None, int] = 10,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    """## Pulls events from a stream

      Pulls events from a stream

    ### Args:
    * `stream_id`: stream_id (str):
    * `count`: count (Union[Unset, None, int]):  Default: 10.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Any, List['OctostarEvent'], PullEventsFromStreamResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        stream_id=stream_id,
        client=client,
        count=count,
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
    count: Union[Unset, None, int] = 10,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    """## Pulls events from a stream

      Pulls events from a stream

    ### Args:
    * `stream_id`: stream_id (str):
    * `count`: count (Union[Unset, None, int]):  Default: 10.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Any, List['OctostarEvent'], PullEventsFromStreamResponse401]`
    """

    return sync_detailed(
        stream_id=stream_id,
        client=client,
        count=count,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    stream_id: str,
    *,
    client: Client = None,
    count: Union[Unset, None, int] = 10,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    """## Pulls events from a stream

      Pulls events from a stream

    ### Args:
    * `stream_id`: stream_id (str):
    * `count`: count (Union[Unset, None, int]):  Default: 10.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Any, List['OctostarEvent'], PullEventsFromStreamResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        stream_id=stream_id,
        client=client,
        count=count,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    stream_id: str,
    *,
    client: Client = None,
    count: Union[Unset, None, int] = 10,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Any, List["OctostarEvent"], PullEventsFromStreamResponse401]]:
    """## Pulls events from a stream

      Pulls events from a stream

    ### Args:
    * `stream_id`: stream_id (str):
    * `count`: count (Union[Unset, None, int]):  Default: 10.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Any, List['OctostarEvent'], PullEventsFromStreamResponse401]`
    """

    return (
        await asyncio_detailed(
            stream_id=stream_id,
            client=client,
            count=count,
            accept=accept,
        )
    ).parsed
