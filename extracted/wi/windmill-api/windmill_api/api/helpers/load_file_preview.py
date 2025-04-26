from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.load_file_preview_response_200 import LoadFilePreviewResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    file_key: str,
    file_size_in_bytes: Union[Unset, None, int] = UNSET,
    file_mime_type: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
    csv_has_header: Union[Unset, None, bool] = UNSET,
    read_bytes_from: Union[Unset, None, int] = UNSET,
    read_bytes_length: Union[Unset, None, int] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["file_key"] = file_key

    params["file_size_in_bytes"] = file_size_in_bytes

    params["file_mime_type"] = file_mime_type

    params["csv_separator"] = csv_separator

    params["csv_has_header"] = csv_has_header

    params["read_bytes_from"] = read_bytes_from

    params["read_bytes_length"] = read_bytes_length

    params["storage"] = storage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/load_file_preview".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[LoadFilePreviewResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LoadFilePreviewResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LoadFilePreviewResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    file_size_in_bytes: Union[Unset, None, int] = UNSET,
    file_mime_type: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
    csv_has_header: Union[Unset, None, bool] = UNSET,
    read_bytes_from: Union[Unset, None, int] = UNSET,
    read_bytes_length: Union[Unset, None, int] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadFilePreviewResponse200]:
    """Load a preview of the file

    Args:
        workspace (str):
        file_key (str):
        file_size_in_bytes (Union[Unset, None, int]):
        file_mime_type (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):
        csv_has_header (Union[Unset, None, bool]):
        read_bytes_from (Union[Unset, None, int]):
        read_bytes_length (Union[Unset, None, int]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadFilePreviewResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        file_size_in_bytes=file_size_in_bytes,
        file_mime_type=file_mime_type,
        csv_separator=csv_separator,
        csv_has_header=csv_has_header,
        read_bytes_from=read_bytes_from,
        read_bytes_length=read_bytes_length,
        storage=storage,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    file_size_in_bytes: Union[Unset, None, int] = UNSET,
    file_mime_type: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
    csv_has_header: Union[Unset, None, bool] = UNSET,
    read_bytes_from: Union[Unset, None, int] = UNSET,
    read_bytes_length: Union[Unset, None, int] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadFilePreviewResponse200]:
    """Load a preview of the file

    Args:
        workspace (str):
        file_key (str):
        file_size_in_bytes (Union[Unset, None, int]):
        file_mime_type (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):
        csv_has_header (Union[Unset, None, bool]):
        read_bytes_from (Union[Unset, None, int]):
        read_bytes_length (Union[Unset, None, int]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadFilePreviewResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        file_key=file_key,
        file_size_in_bytes=file_size_in_bytes,
        file_mime_type=file_mime_type,
        csv_separator=csv_separator,
        csv_has_header=csv_has_header,
        read_bytes_from=read_bytes_from,
        read_bytes_length=read_bytes_length,
        storage=storage,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    file_size_in_bytes: Union[Unset, None, int] = UNSET,
    file_mime_type: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
    csv_has_header: Union[Unset, None, bool] = UNSET,
    read_bytes_from: Union[Unset, None, int] = UNSET,
    read_bytes_length: Union[Unset, None, int] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadFilePreviewResponse200]:
    """Load a preview of the file

    Args:
        workspace (str):
        file_key (str):
        file_size_in_bytes (Union[Unset, None, int]):
        file_mime_type (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):
        csv_has_header (Union[Unset, None, bool]):
        read_bytes_from (Union[Unset, None, int]):
        read_bytes_length (Union[Unset, None, int]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadFilePreviewResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        file_size_in_bytes=file_size_in_bytes,
        file_mime_type=file_mime_type,
        csv_separator=csv_separator,
        csv_has_header=csv_has_header,
        read_bytes_from=read_bytes_from,
        read_bytes_length=read_bytes_length,
        storage=storage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    file_size_in_bytes: Union[Unset, None, int] = UNSET,
    file_mime_type: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
    csv_has_header: Union[Unset, None, bool] = UNSET,
    read_bytes_from: Union[Unset, None, int] = UNSET,
    read_bytes_length: Union[Unset, None, int] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadFilePreviewResponse200]:
    """Load a preview of the file

    Args:
        workspace (str):
        file_key (str):
        file_size_in_bytes (Union[Unset, None, int]):
        file_mime_type (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):
        csv_has_header (Union[Unset, None, bool]):
        read_bytes_from (Union[Unset, None, int]):
        read_bytes_length (Union[Unset, None, int]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadFilePreviewResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            file_key=file_key,
            file_size_in_bytes=file_size_in_bytes,
            file_mime_type=file_mime_type,
            csv_separator=csv_separator,
            csv_has_header=csv_has_header,
            read_bytes_from=read_bytes_from,
            read_bytes_length=read_bytes_length,
            storage=storage,
        )
    ).parsed
