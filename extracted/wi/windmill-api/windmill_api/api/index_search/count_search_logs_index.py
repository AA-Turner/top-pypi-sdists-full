import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.count_search_logs_index_response_200 import CountSearchLogsIndexResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search_query: str,
    min_ts: Union[Unset, None, datetime.datetime] = UNSET,
    max_ts: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["search_query"] = search_query

    json_min_ts: Union[Unset, None, str] = UNSET
    if not isinstance(min_ts, Unset):
        json_min_ts = min_ts.isoformat() if min_ts else None

    params["min_ts"] = json_min_ts

    json_max_ts: Union[Unset, None, str] = UNSET
    if not isinstance(max_ts, Unset):
        json_max_ts = max_ts.isoformat() if max_ts else None

    params["max_ts"] = json_max_ts

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/srch/index/search/count_service_logs",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CountSearchLogsIndexResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CountSearchLogsIndexResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CountSearchLogsIndexResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    min_ts: Union[Unset, None, datetime.datetime] = UNSET,
    max_ts: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[CountSearchLogsIndexResponse200]:
    """Search and count the log line hits on every provided host

    Args:
        search_query (str):
        min_ts (Union[Unset, None, datetime.datetime]):
        max_ts (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CountSearchLogsIndexResponse200]
    """

    kwargs = _get_kwargs(
        search_query=search_query,
        min_ts=min_ts,
        max_ts=max_ts,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    min_ts: Union[Unset, None, datetime.datetime] = UNSET,
    max_ts: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[CountSearchLogsIndexResponse200]:
    """Search and count the log line hits on every provided host

    Args:
        search_query (str):
        min_ts (Union[Unset, None, datetime.datetime]):
        max_ts (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CountSearchLogsIndexResponse200
    """

    return sync_detailed(
        client=client,
        search_query=search_query,
        min_ts=min_ts,
        max_ts=max_ts,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    min_ts: Union[Unset, None, datetime.datetime] = UNSET,
    max_ts: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[CountSearchLogsIndexResponse200]:
    """Search and count the log line hits on every provided host

    Args:
        search_query (str):
        min_ts (Union[Unset, None, datetime.datetime]):
        max_ts (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CountSearchLogsIndexResponse200]
    """

    kwargs = _get_kwargs(
        search_query=search_query,
        min_ts=min_ts,
        max_ts=max_ts,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    min_ts: Union[Unset, None, datetime.datetime] = UNSET,
    max_ts: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[CountSearchLogsIndexResponse200]:
    """Search and count the log line hits on every provided host

    Args:
        search_query (str):
        min_ts (Union[Unset, None, datetime.datetime]):
        max_ts (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CountSearchLogsIndexResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            search_query=search_query,
            min_ts=min_ts,
            max_ts=max_ts,
        )
    ).parsed
