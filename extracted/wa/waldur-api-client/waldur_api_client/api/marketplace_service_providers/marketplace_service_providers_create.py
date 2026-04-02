from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider import ServiceProvider
from ...models.service_provider_request import ServiceProviderRequest
from ...models.service_provider_request_form import ServiceProviderRequestForm
from ...models.service_provider_request_multipart import ServiceProviderRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        ServiceProviderRequest,
        ServiceProviderRequestForm,
        ServiceProviderRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-service-providers/",
    }

    if isinstance(body, ServiceProviderRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ServiceProviderRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ServiceProviderRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ServiceProvider:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ServiceProvider.from_dict(response.json())

        return response_201
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
    *,
    client: AuthenticatedClient,
    body: Union[
        ServiceProviderRequest,
        ServiceProviderRequestForm,
        ServiceProviderRequestMultipart,
    ],
) -> Response[ServiceProvider]:
    """Create a service provider

     Creates a new service provider profile for a customer.

    Args:
        body (ServiceProviderRequest):
        body (ServiceProviderRequestForm):
        body (ServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProvider]
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
    body: Union[
        ServiceProviderRequest,
        ServiceProviderRequestForm,
        ServiceProviderRequestMultipart,
    ],
) -> ServiceProvider:
    """Create a service provider

     Creates a new service provider profile for a customer.

    Args:
        body (ServiceProviderRequest):
        body (ServiceProviderRequestForm):
        body (ServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProvider
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ServiceProviderRequest,
        ServiceProviderRequestForm,
        ServiceProviderRequestMultipart,
    ],
) -> Response[ServiceProvider]:
    """Create a service provider

     Creates a new service provider profile for a customer.

    Args:
        body (ServiceProviderRequest):
        body (ServiceProviderRequestForm):
        body (ServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProvider]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        ServiceProviderRequest,
        ServiceProviderRequestForm,
        ServiceProviderRequestMultipart,
    ],
) -> ServiceProvider:
    """Create a service provider

     Creates a new service provider profile for a customer.

    Args:
        body (ServiceProviderRequest):
        body (ServiceProviderRequestForm):
        body (ServiceProviderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProvider
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
