from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    file_key: str,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["file_key"] = file_key

    params["s3_resource_path"] = s3_resource_path

    params["resource_type"] = resource_type

    params["storage"] = storage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/download_s3_file".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[File]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.content))

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[File]:
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
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[File]:
    """Download file from S3 bucket

    Args:
        workspace (str):
        file_key (str):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
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
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[File]:
    """Download file from S3 bucket

    Args:
        workspace (str):
        file_key (str):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        file_key=file_key,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
        storage=storage,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[File]:
    """Download file from S3 bucket

    Args:
        workspace (str):
        file_key (str):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
        storage=storage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: str,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[File]:
    """Download file from S3 bucket

    Args:
        workspace (str):
        file_key (str):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            file_key=file_key,
            s3_resource_path=s3_resource_path,
            resource_type=resource_type,
            storage=storage,
        )
    ).parsed
