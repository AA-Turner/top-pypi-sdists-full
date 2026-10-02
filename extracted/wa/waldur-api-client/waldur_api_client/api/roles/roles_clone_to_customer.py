from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.role_clone_request import RoleCloneRequest
from ...models.role_details import RoleDetails
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: RoleCloneRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/roles/{uuid}/clone_to_customer/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> RoleDetails:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RoleDetails.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RoleDetails]:
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
    body: RoleCloneRequest,
) -> Response[RoleDetails]:
    """Clone a role into an organization

     Staff-only. Creates an organization-private copy of this role (customer or project scope), bound to
    the given customer and usable only within that organization and its projects. Cloning the same
    template into the same organization twice is rejected.

    Args:
        uuid (UUID):
        body (RoleCloneRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RoleDetails]
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
    body: RoleCloneRequest,
) -> RoleDetails:
    """Clone a role into an organization

     Staff-only. Creates an organization-private copy of this role (customer or project scope), bound to
    the given customer and usable only within that organization and its projects. Cloning the same
    template into the same organization twice is rejected.

    Args:
        uuid (UUID):
        body (RoleCloneRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RoleDetails
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
    body: RoleCloneRequest,
) -> Response[RoleDetails]:
    """Clone a role into an organization

     Staff-only. Creates an organization-private copy of this role (customer or project scope), bound to
    the given customer and usable only within that organization and its projects. Cloning the same
    template into the same organization twice is rejected.

    Args:
        uuid (UUID):
        body (RoleCloneRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RoleDetails]
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
    body: RoleCloneRequest,
) -> RoleDetails:
    """Clone a role into an organization

     Staff-only. Creates an organization-private copy of this role (customer or project scope), bound to
    the given customer and usable only within that organization and its projects. Cloning the same
    template into the same organization twice is rejected.

    Args:
        uuid (UUID):
        body (RoleCloneRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RoleDetails
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
