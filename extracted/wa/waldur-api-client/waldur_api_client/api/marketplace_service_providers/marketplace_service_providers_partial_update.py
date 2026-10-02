from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_service_provider_request import PatchedServiceProviderRequest
from ...models.patched_service_provider_request_form import PatchedServiceProviderRequestForm
from ...models.patched_service_provider_request_multipart import PatchedServiceProviderRequestMultipart
from ...models.service_provider import ServiceProvider
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        PatchedServiceProviderRequest,
        PatchedServiceProviderRequestForm,
        PatchedServiceProviderRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/marketplace-service-providers/{uuid}/",
    }

    if isinstance(body, PatchedServiceProviderRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedServiceProviderRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedServiceProviderRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ServiceProvider:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ServiceProvider.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ServiceProvider]:
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
        PatchedServiceProviderRequest,
        PatchedServiceProviderRequestForm,
        PatchedServiceProviderRequestMultipart,
    ],
) -> Response[ServiceProvider]:
    """Partially update a service provider

     Partially updates an existing service provider profile.

    Args:
        uuid (UUID):
        body (PatchedServiceProviderRequest):
        body (PatchedServiceProviderRequestForm):
        body (PatchedServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProvider]
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
    body: Union[
        PatchedServiceProviderRequest,
        PatchedServiceProviderRequestForm,
        PatchedServiceProviderRequestMultipart,
    ],
) -> ServiceProvider:
    """Partially update a service provider

     Partially updates an existing service provider profile.

    Args:
        uuid (UUID):
        body (PatchedServiceProviderRequest):
        body (PatchedServiceProviderRequestForm):
        body (PatchedServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProvider
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
    body: Union[
        PatchedServiceProviderRequest,
        PatchedServiceProviderRequestForm,
        PatchedServiceProviderRequestMultipart,
    ],
) -> Response[ServiceProvider]:
    """Partially update a service provider

     Partially updates an existing service provider profile.

    Args:
        uuid (UUID):
        body (PatchedServiceProviderRequest):
        body (PatchedServiceProviderRequestForm):
        body (PatchedServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProvider]
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
    body: Union[
        PatchedServiceProviderRequest,
        PatchedServiceProviderRequestForm,
        PatchedServiceProviderRequestMultipart,
    ],
) -> ServiceProvider:
    """Partially update a service provider

     Partially updates an existing service provider profile.

    Args:
        uuid (UUID):
        body (PatchedServiceProviderRequest):
        body (PatchedServiceProviderRequestForm):
        body (PatchedServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProvider
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
