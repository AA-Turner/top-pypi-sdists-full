from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_type_enum import ExportTypeEnum
from ...models.matrix_history_export_state_enum import MatrixHistoryExportStateEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    export_type: Union[Unset, ExportTypeEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    room_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MatrixHistoryExportStateEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_export_type: Union[Unset, str] = UNSET
    if not isinstance(export_type, Unset):
        json_export_type = export_type.value

    params["export_type"] = json_export_type

    params["page"] = page

    params["page_size"] = page_size

    json_room_uuid: Union[Unset, str] = UNSET
    if not isinstance(room_uuid, Unset):
        json_room_uuid = str(room_uuid)
    params["room_uuid"] = json_room_uuid

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/matrix/exports/",
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
    export_type: Union[Unset, ExportTypeEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    room_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MatrixHistoryExportStateEnum] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        export_type (Union[Unset, ExportTypeEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        room_uuid (Union[Unset, UUID]):
        state (Union[Unset, MatrixHistoryExportStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        export_type=export_type,
        page=page,
        page_size=page_size,
        room_uuid=room_uuid,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    export_type: Union[Unset, ExportTypeEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    room_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MatrixHistoryExportStateEnum] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        export_type (Union[Unset, ExportTypeEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        room_uuid (Union[Unset, UUID]):
        state (Union[Unset, MatrixHistoryExportStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        export_type=export_type,
        page=page,
        page_size=page_size,
        room_uuid=room_uuid,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    export_type: Union[Unset, ExportTypeEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    room_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MatrixHistoryExportStateEnum] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        export_type (Union[Unset, ExportTypeEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        room_uuid (Union[Unset, UUID]):
        state (Union[Unset, MatrixHistoryExportStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        export_type=export_type,
        page=page,
        page_size=page_size,
        room_uuid=room_uuid,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    export_type: Union[Unset, ExportTypeEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    room_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MatrixHistoryExportStateEnum] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        export_type (Union[Unset, ExportTypeEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        room_uuid (Union[Unset, UUID]):
        state (Union[Unset, MatrixHistoryExportStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            export_type=export_type,
            page=page,
            page_size=page_size,
            room_uuid=room_uuid,
            state=state,
        )
    ).parsed
