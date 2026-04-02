from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_resources_set_restrict_member_access_response_200 import (
    MarketplaceResourcesSetRestrictMemberAccessResponse200,
)
from ...models.resource_restrict_member_access_request import ResourceRestrictMemberAccessRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceRestrictMemberAccessRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resources/{uuid}/set_restrict_member_access/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MarketplaceResourcesSetRestrictMemberAccessResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceResourcesSetRestrictMemberAccessResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MarketplaceResourcesSetRestrictMemberAccessResponse200]:
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
    body: ResourceRestrictMemberAccessRequest,
) -> Response[MarketplaceResourcesSetRestrictMemberAccessResponse200]:
    """Set restrict member access flag

     Sets the 'restrict_member_access' flag for a resource. Requires staff permissions.

    Args:
        uuid (UUID):
        body (ResourceRestrictMemberAccessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceResourcesSetRestrictMemberAccessResponse200]
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
    body: ResourceRestrictMemberAccessRequest,
) -> MarketplaceResourcesSetRestrictMemberAccessResponse200:
    """Set restrict member access flag

     Sets the 'restrict_member_access' flag for a resource. Requires staff permissions.

    Args:
        uuid (UUID):
        body (ResourceRestrictMemberAccessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceResourcesSetRestrictMemberAccessResponse200
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
    body: ResourceRestrictMemberAccessRequest,
) -> Response[MarketplaceResourcesSetRestrictMemberAccessResponse200]:
    """Set restrict member access flag

     Sets the 'restrict_member_access' flag for a resource. Requires staff permissions.

    Args:
        uuid (UUID):
        body (ResourceRestrictMemberAccessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceResourcesSetRestrictMemberAccessResponse200]
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
    body: ResourceRestrictMemberAccessRequest,
) -> MarketplaceResourcesSetRestrictMemberAccessResponse200:
    """Set restrict member access flag

     Sets the 'restrict_member_access' flag for a resource. Requires staff permissions.

    Args:
        uuid (UUID):
        body (ResourceRestrictMemberAccessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceResourcesSetRestrictMemberAccessResponse200
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
