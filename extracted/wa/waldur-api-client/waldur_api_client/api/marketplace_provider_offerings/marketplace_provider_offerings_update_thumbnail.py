from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_thumbnail_request import OfferingThumbnailRequest
from ...models.offering_thumbnail_request_form import OfferingThumbnailRequestForm
from ...models.offering_thumbnail_request_multipart import OfferingThumbnailRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        OfferingThumbnailRequest,
        OfferingThumbnailRequestForm,
        OfferingThumbnailRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-offerings/{uuid}/update_thumbnail/",
    }

    if isinstance(body, OfferingThumbnailRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, OfferingThumbnailRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, OfferingThumbnailRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        return None
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: Union[
        OfferingThumbnailRequest,
        OfferingThumbnailRequestForm,
        OfferingThumbnailRequestMultipart,
    ],
) -> Response[Any]:
    """Update offering thumbnail

     Uploads or replaces the thumbnail image for an offering.

    Args:
        uuid (UUID):
        body (OfferingThumbnailRequest):
        body (OfferingThumbnailRequestForm):
        body (OfferingThumbnailRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: Union[
        OfferingThumbnailRequest,
        OfferingThumbnailRequestForm,
        OfferingThumbnailRequestMultipart,
    ],
) -> Response[Any]:
    """Update offering thumbnail

     Uploads or replaces the thumbnail image for an offering.

    Args:
        uuid (UUID):
        body (OfferingThumbnailRequest):
        body (OfferingThumbnailRequestForm):
        body (OfferingThumbnailRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
