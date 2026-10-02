import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["event_type"] = event_type

    params["managed_project_destination"] = managed_project_destination

    params["managed_project_identifier"] = managed_project_identifier

    params["o"] = o

    params["page"] = page

    params["page_size"] = page_size

    params["q"] = q

    json_timestamp_after: Union[Unset, str] = UNSET
    if not isinstance(timestamp_after, Unset):
        json_timestamp_after = timestamp_after.isoformat()
    params["timestamp_after"] = json_timestamp_after

    json_timestamp_before: Union[Unset, str] = UNSET
    if not isinstance(timestamp_before, Unset):
        json_timestamp_before = timestamp_before.isoformat()
    params["timestamp_before"] = json_timestamp_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openportal-managed-project-audit/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            event_type=event_type,
            managed_project_destination=managed_project_destination,
            managed_project_identifier=managed_project_identifier,
            o=o,
            page=page,
            page_size=page_size,
            q=q,
            timestamp_after=timestamp_after,
            timestamp_before=timestamp_before,
        )
    ).parsed
