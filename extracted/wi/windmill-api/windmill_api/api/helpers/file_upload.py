from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.file_upload_response_200 import FileUploadResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    file_key: Union[Unset, None, str] = UNSET,
    file_extension: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["file_key"] = file_key

    params["file_extension"] = file_extension

    params["s3_resource_path"] = s3_resource_path

    params["resource_type"] = resource_type

    params["storage"] = storage

    params["content_type"] = content_type

    params["content_disposition"] = content_disposition

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/job_helpers/upload_s3_file".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[FileUploadResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = FileUploadResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[FileUploadResponse200]:
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
    file_key: Union[Unset, None, str] = UNSET,
    file_extension: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
) -> Response[FileUploadResponse200]:
    """Upload file to S3 bucket

    Args:
        workspace (str):
        file_key (Union[Unset, None, str]):
        file_extension (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        content_type (Union[Unset, None, str]):
        content_disposition (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileUploadResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        file_extension=file_extension,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
        storage=storage,
        content_type=content_type,
        content_disposition=content_disposition,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: Union[Unset, None, str] = UNSET,
    file_extension: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
) -> Optional[FileUploadResponse200]:
    """Upload file to S3 bucket

    Args:
        workspace (str):
        file_key (Union[Unset, None, str]):
        file_extension (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        content_type (Union[Unset, None, str]):
        content_disposition (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileUploadResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        file_key=file_key,
        file_extension=file_extension,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
        storage=storage,
        content_type=content_type,
        content_disposition=content_disposition,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: Union[Unset, None, str] = UNSET,
    file_extension: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
) -> Response[FileUploadResponse200]:
    """Upload file to S3 bucket

    Args:
        workspace (str):
        file_key (Union[Unset, None, str]):
        file_extension (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        content_type (Union[Unset, None, str]):
        content_disposition (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileUploadResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        file_key=file_key,
        file_extension=file_extension,
        s3_resource_path=s3_resource_path,
        resource_type=resource_type,
        storage=storage,
        content_type=content_type,
        content_disposition=content_disposition,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    file_key: Union[Unset, None, str] = UNSET,
    file_extension: Union[Unset, None, str] = UNSET,
    s3_resource_path: Union[Unset, None, str] = UNSET,
    resource_type: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, None, str] = UNSET,
    content_disposition: Union[Unset, None, str] = UNSET,
) -> Optional[FileUploadResponse200]:
    """Upload file to S3 bucket

    Args:
        workspace (str):
        file_key (Union[Unset, None, str]):
        file_extension (Union[Unset, None, str]):
        s3_resource_path (Union[Unset, None, str]):
        resource_type (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        content_type (Union[Unset, None, str]):
        content_disposition (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileUploadResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            file_key=file_key,
            file_extension=file_extension,
            s3_resource_path=s3_resource_path,
            resource_type=resource_type,
            storage=storage,
            content_type=content_type,
            content_disposition=content_disposition,
        )
    ).parsed
