from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_google_drive_files_response_200 import ListGoogleDriveFilesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    q: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    page_token: Union[Unset, None, str] = UNSET,
    shared_with_me: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["q"] = q

    params["parent_id"] = parent_id

    params["page_token"] = page_token

    params["shared_with_me"] = shared_with_me

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/native_triggers/google/drive/files".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListGoogleDriveFilesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListGoogleDriveFilesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListGoogleDriveFilesResponse200]:
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
    q: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    page_token: Union[Unset, None, str] = UNSET,
    shared_with_me: Union[Unset, None, bool] = False,
) -> Response[ListGoogleDriveFilesResponse200]:
    """list or search Google Drive files

    Args:
        workspace (str):
        q (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        page_token (Union[Unset, None, str]):
        shared_with_me (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListGoogleDriveFilesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        q=q,
        parent_id=parent_id,
        page_token=page_token,
        shared_with_me=shared_with_me,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    page_token: Union[Unset, None, str] = UNSET,
    shared_with_me: Union[Unset, None, bool] = False,
) -> Optional[ListGoogleDriveFilesResponse200]:
    """list or search Google Drive files

    Args:
        workspace (str):
        q (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        page_token (Union[Unset, None, str]):
        shared_with_me (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListGoogleDriveFilesResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        q=q,
        parent_id=parent_id,
        page_token=page_token,
        shared_with_me=shared_with_me,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    page_token: Union[Unset, None, str] = UNSET,
    shared_with_me: Union[Unset, None, bool] = False,
) -> Response[ListGoogleDriveFilesResponse200]:
    """list or search Google Drive files

    Args:
        workspace (str):
        q (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        page_token (Union[Unset, None, str]):
        shared_with_me (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListGoogleDriveFilesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        q=q,
        parent_id=parent_id,
        page_token=page_token,
        shared_with_me=shared_with_me,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    q: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    page_token: Union[Unset, None, str] = UNSET,
    shared_with_me: Union[Unset, None, bool] = False,
) -> Optional[ListGoogleDriveFilesResponse200]:
    """list or search Google Drive files

    Args:
        workspace (str):
        q (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        page_token (Union[Unset, None, str]):
        shared_with_me (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListGoogleDriveFilesResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            q=q,
            parent_id=parent_id,
            page_token=page_token,
            shared_with_me=shared_with_me,
        )
    ).parsed
