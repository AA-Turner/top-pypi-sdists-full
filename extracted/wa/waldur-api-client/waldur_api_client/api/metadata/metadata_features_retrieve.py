from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature_metadata_response import FeatureMetadataResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/metadata/features/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> FeatureMetadataResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = FeatureMetadataResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[FeatureMetadataResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[FeatureMetadataResponse]:
    """Get feature flag metadata

     Retrieves metadata for all available feature flags, including their keys, descriptions, and grouping
    sections. This endpoint is publicly accessible and helps UIs to dynamically render feature-related
    settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FeatureMetadataResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> FeatureMetadataResponse:
    """Get feature flag metadata

     Retrieves metadata for all available feature flags, including their keys, descriptions, and grouping
    sections. This endpoint is publicly accessible and helps UIs to dynamically render feature-related
    settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FeatureMetadataResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[FeatureMetadataResponse]:
    """Get feature flag metadata

     Retrieves metadata for all available feature flags, including their keys, descriptions, and grouping
    sections. This endpoint is publicly accessible and helps UIs to dynamically render feature-related
    settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FeatureMetadataResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> FeatureMetadataResponse:
    """Get feature flag metadata

     Retrieves metadata for all available feature flags, including their keys, descriptions, and grouping
    sections. This endpoint is publicly accessible and helps UIs to dynamically render feature-related
    settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FeatureMetadataResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
