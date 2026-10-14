from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider_project_group import ServiceProviderProjectGroup
from ...models.service_provider_project_group_create_request import ServiceProviderProjectGroupCreateRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ServiceProviderProjectGroupCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-service-provider-project-groups/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ServiceProviderProjectGroup:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ServiceProviderProjectGroup.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ServiceProviderProjectGroup]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ServiceProviderProjectGroupCreateRequest,
) -> Response[ServiceProviderProjectGroup]:
    """Adopt a POSIX project group with a given GID

     Create the service provider's group for a project, pinned to a GID the directory already uses. Works
    for a project that has no resource at the provider yet; the allocator never hands the GID out
    afterwards. Refused with 400 when the project already has a group (use set_gid), when another
    consumer in the provider's pools holds the GID, or when the GID is outside the range project groups
    draw from and allow_outside_range is not set.

    Args:
        body (ServiceProviderProjectGroupCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderProjectGroup]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ServiceProviderProjectGroupCreateRequest,
) -> ServiceProviderProjectGroup:
    """Adopt a POSIX project group with a given GID

     Create the service provider's group for a project, pinned to a GID the directory already uses. Works
    for a project that has no resource at the provider yet; the allocator never hands the GID out
    afterwards. Refused with 400 when the project already has a group (use set_gid), when another
    consumer in the provider's pools holds the GID, or when the GID is outside the range project groups
    draw from and allow_outside_range is not set.

    Args:
        body (ServiceProviderProjectGroupCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderProjectGroup
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ServiceProviderProjectGroupCreateRequest,
) -> Response[ServiceProviderProjectGroup]:
    """Adopt a POSIX project group with a given GID

     Create the service provider's group for a project, pinned to a GID the directory already uses. Works
    for a project that has no resource at the provider yet; the allocator never hands the GID out
    afterwards. Refused with 400 when the project already has a group (use set_gid), when another
    consumer in the provider's pools holds the GID, or when the GID is outside the range project groups
    draw from and allow_outside_range is not set.

    Args:
        body (ServiceProviderProjectGroupCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderProjectGroup]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ServiceProviderProjectGroupCreateRequest,
) -> ServiceProviderProjectGroup:
    """Adopt a POSIX project group with a given GID

     Create the service provider's group for a project, pinned to a GID the directory already uses. Works
    for a project that has no resource at the provider yet; the allocator never hands the GID out
    afterwards. Refused with 400 when the project already has a group (use set_gid), when another
    consumer in the provider's pools holds the GID, or when the GID is outside the range project groups
    draw from and allow_outside_range is not set.

    Args:
        body (ServiceProviderProjectGroupCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderProjectGroup
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
