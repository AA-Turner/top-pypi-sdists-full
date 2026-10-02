from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_user_attribute_config import OfferingUserAttributeConfig
from ...models.patched_offering_user_attribute_config_request import PatchedOfferingUserAttributeConfigRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: PatchedOfferingUserAttributeConfigRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/marketplace-provider-offerings/{uuid}/update-user-attribute-config/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> OfferingUserAttributeConfig:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingUserAttributeConfig.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingUserAttributeConfig]:
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
    body: PatchedOfferingUserAttributeConfigRequest,
) -> Response[OfferingUserAttributeConfig]:
    """Update user attribute config

     Creates or updates the user attribute configuration for this offering. This determines which user
    attributes are shared with the service provider.

    Args:
        uuid (UUID):
        body (PatchedOfferingUserAttributeConfigRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUserAttributeConfig]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedOfferingUserAttributeConfigRequest,
) -> OfferingUserAttributeConfig:
    """Update user attribute config

     Creates or updates the user attribute configuration for this offering. This determines which user
    attributes are shared with the service provider.

    Args:
        uuid (UUID):
        body (PatchedOfferingUserAttributeConfigRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUserAttributeConfig
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedOfferingUserAttributeConfigRequest,
) -> Response[OfferingUserAttributeConfig]:
    """Update user attribute config

     Creates or updates the user attribute configuration for this offering. This determines which user
    attributes are shared with the service provider.

    Args:
        uuid (UUID):
        body (PatchedOfferingUserAttributeConfigRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUserAttributeConfig]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedOfferingUserAttributeConfigRequest,
) -> OfferingUserAttributeConfig:
    """Update user attribute config

     Creates or updates the user attribute configuration for this offering. This determines which user
    attributes are shared with the service provider.

    Args:
        uuid (UUID):
        body (PatchedOfferingUserAttributeConfigRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUserAttributeConfig
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
