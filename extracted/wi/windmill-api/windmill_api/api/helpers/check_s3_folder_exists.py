from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_s3_folder_exists_response_200 import CheckS3FolderExistsResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    file_key: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["file_key"] = file_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/check_s3_folder_exists".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CheckS3FolderExistsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CheckS3FolderExistsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CheckS3FolderExistsResponse200]:
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
) -> Response[CheckS3FolderExistsResponse200]:
    """Check if S3 path exists and is a folder

    Args:
        workspace (str):
        file_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckS3FolderExistsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
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
) -> Optional[CheckS3FolderExistsResponse200]:
    """Check if S3 path exists and is a folder

    Args:
        workspace (str):
        file_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckS3FolderExistsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        file_key=file_key,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
) -> Response[CheckS3FolderExistsResponse200]:
    """Check if S3 path exists and is a folder

    Args:
        workspace (str):
        file_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckS3FolderExistsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
) -> Optional[CheckS3FolderExistsResponse200]:
    """Check if S3 path exists and is a folder

    Args:
        workspace (str):
        file_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckS3FolderExistsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            file_key=file_key,
        )
    ).parsed
