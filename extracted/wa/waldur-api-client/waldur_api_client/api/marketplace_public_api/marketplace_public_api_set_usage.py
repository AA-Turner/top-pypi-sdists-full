from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider_signature_request import ServiceProviderSignatureRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ServiceProviderSignatureRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-public-api/set_usage/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
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
    *,
    client: AuthenticatedClient,
    body: ServiceProviderSignatureRequest,
) -> Response[Any]:
    """Set component usage with signature


            Allows a service provider to report usage for resource components using a signed JWT
    payload.
            This provides a secure way for external systems to submit billing data.

            The `data` field must contain a JWT token that, when decoded, matches the structure of the
            `ComponentUsageCreateSerializer`.


    Args:
        body (ServiceProviderSignatureRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ServiceProviderSignatureRequest,
) -> Response[Any]:
    """Set component usage with signature


            Allows a service provider to report usage for resource components using a signed JWT
    payload.
            This provides a secure way for external systems to submit billing data.

            The `data` field must contain a JWT token that, when decoded, matches the structure of the
            `ComponentUsageCreateSerializer`.


    Args:
        body (ServiceProviderSignatureRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
