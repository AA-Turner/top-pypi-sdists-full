import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.schema_detail_response import SchemaDetailResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    dataset_name: str,
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
        "url": "/telemetry/v1/workspaces/{workspace_id}/datasets/{dataset_name}/schema".format(
            workspace_id=quote(str(workspace_id), safe=""),
            dataset_name=quote(str(dataset_name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | SchemaDetailResponse | None:
    if response.status_code == 200:
        response_200 = SchemaDetailResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | SchemaDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    dataset_name: str,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> Response[ErrorResponse400 | SchemaDetailResponse]:
    """GetDatasetSchema

    Args:
        workspace_id (UUID):
        dataset_name (str):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | SchemaDetailResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        dataset_name=dataset_name,
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
    dataset_name: str,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> ErrorResponse400 | SchemaDetailResponse | None:
    """GetDatasetSchema

    Args:
        workspace_id (UUID):
        dataset_name (str):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | SchemaDetailResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        dataset_name=dataset_name,
        client=client,
        start=start,
        end=end,
        tz=tz,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    dataset_name: str,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> Response[ErrorResponse400 | SchemaDetailResponse]:
    """GetDatasetSchema

    Args:
        workspace_id (UUID):
        dataset_name (str):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | SchemaDetailResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        dataset_name=dataset_name,
        start=start,
        end=end,
        tz=tz,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    dataset_name: str,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
) -> ErrorResponse400 | SchemaDetailResponse | None:
    """GetDatasetSchema

    Args:
        workspace_id (UUID):
        dataset_name (str):
        start (datetime.datetime | None | Unset):
        end (datetime.datetime | None | Unset):
        tz (str | Unset):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | SchemaDetailResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            dataset_name=dataset_name,
            client=client,
            start=start,
            end=end,
            tz=tz,
        )
    ).parsed
