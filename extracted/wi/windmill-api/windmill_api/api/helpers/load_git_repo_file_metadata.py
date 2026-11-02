from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.load_git_repo_file_metadata_response_200 import LoadGitRepoFileMetadataResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    file_key: str,
    storage: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["file_key"] = file_key

    params["storage"] = storage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/load_git_repo_file_metadata".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[LoadGitRepoFileMetadataResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LoadGitRepoFileMetadataResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LoadGitRepoFileMetadataResponse200]:
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
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadGitRepoFileMetadataResponse200]:
    """Load file metadata from instance storage with resource-based access control

    Args:
        workspace (str):
        file_key (str): Must follow format gitrepos/{workspace_id}/{resource_path}/...
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadGitRepoFileMetadataResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
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
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadGitRepoFileMetadataResponse200]:
    """Load file metadata from instance storage with resource-based access control

    Args:
        workspace (str):
        file_key (str): Must follow format gitrepos/{workspace_id}/{resource_path}/...
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadGitRepoFileMetadataResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        file_key=file_key,
        storage=storage,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadGitRepoFileMetadataResponse200]:
    """Load file metadata from instance storage with resource-based access control

    Args:
        workspace (str):
        file_key (str): Must follow format gitrepos/{workspace_id}/{resource_path}/...
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadGitRepoFileMetadataResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        storage=storage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadGitRepoFileMetadataResponse200]:
    """Load file metadata from instance storage with resource-based access control

    Args:
        workspace (str):
        file_key (str): Must follow format gitrepos/{workspace_id}/{resource_path}/...
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadGitRepoFileMetadataResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            file_key=file_key,
            storage=storage,
        )
    ).parsed
