from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.image_upload_response import ImageUploadResponse
from ...types import File, Response


def _get_kwargs(
    uuid: UUID,
    image_id: UUID,
    *,
    body: File,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openstack-marketplace-tenants/{uuid}/upload_image_data/{image_id}/",
    }

    _kwargs["json"] = body.to_tuple()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ImageUploadResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ImageUploadResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ImageUploadResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    image_id: UUID,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[ImageUploadResponse]:
    """
    Args:
        uuid (UUID):
        image_id (UUID):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImageUploadResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        image_id=image_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    image_id: UUID,
    *,
    client: AuthenticatedClient,
    body: File,
) -> ImageUploadResponse:
    """
    Args:
        uuid (UUID):
        image_id (UUID):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImageUploadResponse
    """

    return sync_detailed(
        uuid=uuid,
        image_id=image_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    image_id: UUID,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[ImageUploadResponse]:
    """
    Args:
        uuid (UUID):
        image_id (UUID):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImageUploadResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        image_id=image_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    image_id: UUID,
    *,
    client: AuthenticatedClient,
    body: File,
) -> ImageUploadResponse:
    """
    Args:
        uuid (UUID):
        image_id (UUID):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImageUploadResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            image_id=image_id,
            client=client,
            body=body,
        )
    ).parsed
