import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_log_files_response_200_item import ListLogFilesResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_error: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_before: Union[Unset, None, str] = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat() if before else None

    params["before"] = json_before

    json_after: Union[Unset, None, str] = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat() if after else None

    params["after"] = json_after

    params["with_error"] = with_error

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/service_logs/list_files",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListLogFilesResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListLogFilesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListLogFilesResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_error: Union[Unset, None, bool] = UNSET,
) -> Response[List["ListLogFilesResponse200Item"]]:
    """list log files ordered by timestamp

    Args:
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_error (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListLogFilesResponse200Item']]
    """

    kwargs = _get_kwargs(
        before=before,
        after=after,
        with_error=with_error,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_error: Union[Unset, None, bool] = UNSET,
) -> Optional[List["ListLogFilesResponse200Item"]]:
    """list log files ordered by timestamp

    Args:
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_error (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListLogFilesResponse200Item']
    """

    return sync_detailed(
        client=client,
        before=before,
        after=after,
        with_error=with_error,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_error: Union[Unset, None, bool] = UNSET,
) -> Response[List["ListLogFilesResponse200Item"]]:
    """list log files ordered by timestamp

    Args:
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_error (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListLogFilesResponse200Item']]
    """

    kwargs = _get_kwargs(
        before=before,
        after=after,
        with_error=with_error,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    before: Union[Unset, None, datetime.datetime] = UNSET,
    after: Union[Unset, None, datetime.datetime] = UNSET,
    with_error: Union[Unset, None, bool] = UNSET,
) -> Optional[List["ListLogFilesResponse200Item"]]:
    """list log files ordered by timestamp

    Args:
        before (Union[Unset, None, datetime.datetime]):
        after (Union[Unset, None, datetime.datetime]):
        with_error (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListLogFilesResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            before=before,
            after=after,
            with_error=with_error,
        )
    ).parsed
