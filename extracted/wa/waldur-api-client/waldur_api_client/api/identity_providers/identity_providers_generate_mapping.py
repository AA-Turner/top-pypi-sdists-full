from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.discover_metadata_request_request import DiscoverMetadataRequestRequest
from ...models.identity_providers_generate_mapping_response_200 import IdentityProvidersGenerateMappingResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: DiscoverMetadataRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/identity-providers/generate-mapping/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> IdentityProvidersGenerateMappingResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = IdentityProvidersGenerateMappingResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[IdentityProvidersGenerateMappingResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DiscoverMetadataRequestRequest,
) -> Response[IdentityProvidersGenerateMappingResponse200]:
    """Generate default attribute mapping

     Generates a suggested attribute_mapping configuration based on the claims supported by an OIDC
    provider. This can be used as a starting point when creating a new identity provider.

    Args:
        body (DiscoverMetadataRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityProvidersGenerateMappingResponse200]
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
    body: DiscoverMetadataRequestRequest,
) -> IdentityProvidersGenerateMappingResponse200:
    """Generate default attribute mapping

     Generates a suggested attribute_mapping configuration based on the claims supported by an OIDC
    provider. This can be used as a starting point when creating a new identity provider.

    Args:
        body (DiscoverMetadataRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityProvidersGenerateMappingResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DiscoverMetadataRequestRequest,
) -> Response[IdentityProvidersGenerateMappingResponse200]:
    """Generate default attribute mapping

     Generates a suggested attribute_mapping configuration based on the claims supported by an OIDC
    provider. This can be used as a starting point when creating a new identity provider.

    Args:
        body (DiscoverMetadataRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityProvidersGenerateMappingResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: DiscoverMetadataRequestRequest,
) -> IdentityProvidersGenerateMappingResponse200:
    """Generate default attribute mapping

     Generates a suggested attribute_mapping configuration based on the claims supported by an OIDC
    provider. This can be used as a starting point when creating a new identity provider.

    Args:
        body (DiscoverMetadataRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityProvidersGenerateMappingResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
