from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_stored_files_paged_response_200 import ListStoredFilesPagedResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    prefix: Union[Unset, None, str] = UNSET,
    max_keys: Union[Unset, None, int] = 100,
    page_token: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["prefix"] = prefix

    params["max_keys"] = max_keys

    params["page_token"] = page_token

    params["storage"] = storage

    params["s3_resource_path"] = s3_resource_path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/list_stored_files_paged".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListStoredFilesPagedResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListStoredFilesPagedResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListStoredFilesPagedResponse200]:
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
    prefix: Union[Unset, None, str] = UNSET,
    max_keys: Union[Unset, None, int] = 100,
    page_token: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
) -> Response[ListStoredFilesPagedResponse200]:
    """List one page of a single folder level in a workspace object storage

    Args:
        workspace (str):
        prefix (Union[Unset, None, str]):
        max_keys (Union[Unset, None, int]):  Default: 100.
        page_token (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListStoredFilesPagedResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        prefix=prefix,
        max_keys=max_keys,
        page_token=page_token,
        storage=storage,
        s3_resource_path=s3_resource_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    prefix: Union[Unset, None, str] = UNSET,
    max_keys: Union[Unset, None, int] = 100,
    page_token: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
) -> Optional[ListStoredFilesPagedResponse200]:
    """List one page of a single folder level in a workspace object storage

    Args:
        workspace (str):
        prefix (Union[Unset, None, str]):
        max_keys (Union[Unset, None, int]):  Default: 100.
        page_token (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListStoredFilesPagedResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        prefix=prefix,
        max_keys=max_keys,
        page_token=page_token,
        storage=storage,
        s3_resource_path=s3_resource_path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    prefix: Union[Unset, None, str] = UNSET,
    max_keys: Union[Unset, None, int] = 100,
    page_token: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
) -> Response[ListStoredFilesPagedResponse200]:
    """List one page of a single folder level in a workspace object storage

    Args:
        workspace (str):
        prefix (Union[Unset, None, str]):
        max_keys (Union[Unset, None, int]):  Default: 100.
        page_token (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListStoredFilesPagedResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        prefix=prefix,
        max_keys=max_keys,
        page_token=page_token,
        storage=storage,
        s3_resource_path=s3_resource_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    prefix: Union[Unset, None, str] = UNSET,
    max_keys: Union[Unset, None, int] = 100,
    page_token: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
) -> Optional[ListStoredFilesPagedResponse200]:
    """List one page of a single folder level in a workspace object storage

    Args:
        workspace (str):
        prefix (Union[Unset, None, str]):
        max_keys (Union[Unset, None, int]):  Default: 100.
        page_token (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListStoredFilesPagedResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            prefix=prefix,
            max_keys=max_keys,
            page_token=page_token,
            storage=storage,
            s3_resource_path=s3_resource_path,
        )
    ).parsed
