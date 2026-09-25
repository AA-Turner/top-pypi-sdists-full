import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.run_facets import RunFacets
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start: None | str | Unset
    if isinstance(start, Unset):
        json_start = UNSET
    elif isinstance(start, datetime.datetime):
        json_start = start.isoformat()
    else:
        json_start = start
    params["start"] = json_start

    json_end: None | str | Unset
    if isinstance(end, Unset):
        json_end = UNSET
    elif isinstance(end, datetime.datetime):
        json_end = end.isoformat()
    else:
        json_end = end
    params["end"] = json_end

    params["tz"] = tz

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/facets/runs".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
    | None
):
    if response.status_code == 200:
        response_200 = RunFacets.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
]:
    """ListRunFacets

    Gets the options the job run list's open-ended filters can take, each with the
    number of rows carrying it. Filters whose domain is a closed enum are absent,
    since their values are already in this API's schema.

    A facet lists the values present in the data, so a value it omits is still
    accepted by the filter and simply matches nothing.

    Accepts the same optional `start`, `end` and `tz` window as the list, so the
    options and counts can be narrowed to the period on screen.

    Requires READ permission on the workspace level.

    Args:
        workspace_id (UUID):
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunFacets]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        start=start,
        end=end,
        tz=tz,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
    | None
):
    """ListRunFacets

    Gets the options the job run list's open-ended filters can take, each with the
    number of rows carrying it. Filters whose domain is a closed enum are absent,
    since their values are already in this API's schema.

    A facet lists the values present in the data, so a value it omits is still
    accepted by the filter and simply matches nothing.

    Accepts the same optional `start`, `end` and `tz` window as the list, so the
    options and counts can be narrowed to the period on screen.

    Requires READ permission on the workspace level.

    Args:
        workspace_id (UUID):
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunFacets
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        start=start,
        end=end,
        tz=tz,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
]:
    """ListRunFacets

    Gets the options the job run list's open-ended filters can take, each with the
    number of rows carrying it. Filters whose domain is a closed enum are absent,
    since their values are already in this API's schema.

    A facet lists the values present in the data, so a value it omits is still
    accepted by the filter and simply matches nothing.

    Accepts the same optional `start`, `end` and `tz` window as the list, so the
    options and counts can be narrowed to the period on screen.

    Requires READ permission on the workspace level.

    Args:
        workspace_id (UUID):
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunFacets]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        start=start,
        end=end,
        tz=tz,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunFacets
    | None
):
    """ListRunFacets

    Gets the options the job run list's open-ended filters can take, each with the
    number of rows carrying it. Filters whose domain is a closed enum are absent,
    since their values are already in this API's schema.

    A facet lists the values present in the data, so a value it omits is still
    accepted by the filter and simply matches nothing.

    Accepts the same optional `start`, `end` and `tz` window as the list, so the
    options and counts can be narrowed to the period on screen.

    Requires READ permission on the workspace level.

    Args:
        workspace_id (UUID):
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunFacets
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            start=start,
            end=end,
            tz=tz,
        )
    ).parsed
