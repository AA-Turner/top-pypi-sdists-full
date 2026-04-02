from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_keycloak_scopes_request import ResourceKeycloakScopesRequest
from ...models.resource_response_status import ResourceResponseStatus
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceKeycloakScopesRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-resources/{uuid}/set_keycloak_scopes/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ResourceResponseStatus:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ResourceResponseStatus.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResourceResponseStatus]:
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
    body: ResourceKeycloakScopesRequest,
) -> Response[ResourceResponseStatus]:
    """Set Keycloak scope options for a resource

     Allows a service provider to configure available scope options for Keycloak memberships on a
    resource. Requires Keycloak integration to be enabled on the offering.

    Args:
        uuid (UUID):
        body (ResourceKeycloakScopesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceResponseStatus]
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
    body: ResourceKeycloakScopesRequest,
) -> ResourceResponseStatus:
    """Set Keycloak scope options for a resource

     Allows a service provider to configure available scope options for Keycloak memberships on a
    resource. Requires Keycloak integration to be enabled on the offering.

    Args:
        uuid (UUID):
        body (ResourceKeycloakScopesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceResponseStatus
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
    body: ResourceKeycloakScopesRequest,
) -> Response[ResourceResponseStatus]:
    """Set Keycloak scope options for a resource

     Allows a service provider to configure available scope options for Keycloak memberships on a
    resource. Requires Keycloak integration to be enabled on the offering.

    Args:
        uuid (UUID):
        body (ResourceKeycloakScopesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceResponseStatus]
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
    body: ResourceKeycloakScopesRequest,
) -> ResourceResponseStatus:
    """Set Keycloak scope options for a resource

     Allows a service provider to configure available scope options for Keycloak memberships on a
    resource. Requires Keycloak integration to be enabled on the offering.

    Args:
        uuid (UUID):
        body (ResourceKeycloakScopesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceResponseStatus
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
