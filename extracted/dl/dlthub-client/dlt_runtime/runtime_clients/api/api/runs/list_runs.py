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
from ...models.list_runs_response_200 import ListRunsResponse200
from ...models.run_status import RunStatus
from ...models.run_status_filter import RunStatusFilter
from ...models.script_type import ScriptType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    script_id: None | Unset | UUID = UNSET,
    status: None | RunStatus | Unset = UNSET,
    status_filter: None | RunStatusFilter | Unset = UNSET,
    script_type: None | ScriptType | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    include_system_runs: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_script_id: None | str | Unset
    if isinstance(script_id, Unset):
        json_script_id = UNSET
    elif isinstance(script_id, UUID):
        json_script_id = str(script_id)
    else:
        json_script_id = script_id
    params["script_id"] = json_script_id

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, RunStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_status_filter: None | str | Unset
    if isinstance(status_filter, Unset):
        json_status_filter = UNSET
    elif isinstance(status_filter, RunStatusFilter):
        json_status_filter = status_filter.value
    else:
        json_status_filter = status_filter
    params["status_filter"] = json_status_filter

    json_script_type: None | str | Unset
    if isinstance(script_type, Unset):
        json_script_type = UNSET
    elif isinstance(script_type, ScriptType):
        json_script_type = script_type.value
    else:
        json_script_type = script_type
    params["script_type"] = json_script_type

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

    params["include_system_runs"] = include_system_runs

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/runs".format(
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
    | ListRunsResponse200
    | None
):
    if response.status_code == 200:
        response_200 = ListRunsResponse200.from_dict(response.json())

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
    | ListRunsResponse200
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
    script_id: None | Unset | UUID = UNSET,
    status: None | RunStatus | Unset = UNSET,
    status_filter: None | RunStatusFilter | Unset = UNSET,
    script_type: None | ScriptType | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    include_system_runs: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListRunsResponse200
]:
    """ListRuns


    Gets all runs for a workspace. Returns a paginated list of runs ordered by date_added descending.
    Can be filtered by script ID and status.

    By default, system runs (e.g. dashboard scripts) are excluded unless a specific script_id is
    provided or include_system_runs is set to true.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id (None | Unset | UUID):
        status (None | RunStatus | Unset):
        status_filter (None | RunStatusFilter | Unset):
        script_type (None | ScriptType | Unset):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        include_system_runs (bool | Unset):  Default: False.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListRunsResponse200]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id=script_id,
        status=status,
        status_filter=status_filter,
        script_type=script_type,
        start=start,
        end=end,
        tz=tz,
        include_system_runs=include_system_runs,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_id: None | Unset | UUID = UNSET,
    status: None | RunStatus | Unset = UNSET,
    status_filter: None | RunStatusFilter | Unset = UNSET,
    script_type: None | ScriptType | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    include_system_runs: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListRunsResponse200
    | None
):
    """ListRuns


    Gets all runs for a workspace. Returns a paginated list of runs ordered by date_added descending.
    Can be filtered by script ID and status.

    By default, system runs (e.g. dashboard scripts) are excluded unless a specific script_id is
    provided or include_system_runs is set to true.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id (None | Unset | UUID):
        status (None | RunStatus | Unset):
        status_filter (None | RunStatusFilter | Unset):
        script_type (None | ScriptType | Unset):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        include_system_runs (bool | Unset):  Default: False.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListRunsResponse200
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        script_id=script_id,
        status=status,
        status_filter=status_filter,
        script_type=script_type,
        start=start,
        end=end,
        tz=tz,
        include_system_runs=include_system_runs,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_id: None | Unset | UUID = UNSET,
    status: None | RunStatus | Unset = UNSET,
    status_filter: None | RunStatusFilter | Unset = UNSET,
    script_type: None | ScriptType | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    include_system_runs: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListRunsResponse200
]:
    """ListRuns


    Gets all runs for a workspace. Returns a paginated list of runs ordered by date_added descending.
    Can be filtered by script ID and status.

    By default, system runs (e.g. dashboard scripts) are excluded unless a specific script_id is
    provided or include_system_runs is set to true.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id (None | Unset | UUID):
        status (None | RunStatus | Unset):
        status_filter (None | RunStatusFilter | Unset):
        script_type (None | ScriptType | Unset):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        include_system_runs (bool | Unset):  Default: False.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListRunsResponse200]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id=script_id,
        status=status,
        status_filter=status_filter,
        script_type=script_type,
        start=start,
        end=end,
        tz=tz,
        include_system_runs=include_system_runs,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_id: None | Unset | UUID = UNSET,
    status: None | RunStatus | Unset = UNSET,
    status_filter: None | RunStatusFilter | Unset = UNSET,
    script_type: None | ScriptType | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    include_system_runs: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListRunsResponse200
    | None
):
    """ListRuns


    Gets all runs for a workspace. Returns a paginated list of runs ordered by date_added descending.
    Can be filtered by script ID and status.

    By default, system runs (e.g. dashboard scripts) are excluded unless a specific script_id is
    provided or include_system_runs is set to true.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id (None | Unset | UUID):
        status (None | RunStatus | Unset):
        status_filter (None | RunStatusFilter | Unset):
        script_type (None | ScriptType | Unset):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        include_system_runs (bool | Unset):  Default: False.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListRunsResponse200
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            script_id=script_id,
            status=status,
            status_filter=status_filter,
            script_type=script_type,
            start=start,
            end=end,
            tz=tz,
            include_system_runs=include_system_runs,
            limit=limit,
            offset=offset,
        )
    ).parsed
