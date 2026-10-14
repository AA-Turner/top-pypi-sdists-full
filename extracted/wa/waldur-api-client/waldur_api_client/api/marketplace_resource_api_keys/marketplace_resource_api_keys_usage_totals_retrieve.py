from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_usage_totals import ResourceApiKeyUsageTotals
from ...types import UNSET, Response


def _get_kwargs(
    *,
    resource_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-resource-api-keys/usage_totals/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ResourceApiKeyUsageTotals:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ResourceApiKeyUsageTotals.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResourceApiKeyUsageTotals]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    resource_uuid: UUID,
) -> Response[ResourceApiKeyUsageTotals]:
    """Total API key usage of a resource

     Sums the usage the site agent reported for the resource's keys in the current month, per component
    type. Deleted keys are included, so deleting a key leaves the total unchanged.

    Args:
        resource_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyUsageTotals]
    """

    kwargs = _get_kwargs(
        resource_uuid=resource_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    resource_uuid: UUID,
) -> ResourceApiKeyUsageTotals:
    """Total API key usage of a resource

     Sums the usage the site agent reported for the resource's keys in the current month, per component
    type. Deleted keys are included, so deleting a key leaves the total unchanged.

    Args:
        resource_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyUsageTotals
    """

    return sync_detailed(
        client=client,
        resource_uuid=resource_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    resource_uuid: UUID,
) -> Response[ResourceApiKeyUsageTotals]:
    """Total API key usage of a resource

     Sums the usage the site agent reported for the resource's keys in the current month, per component
    type. Deleted keys are included, so deleting a key leaves the total unchanged.

    Args:
        resource_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyUsageTotals]
    """

    kwargs = _get_kwargs(
        resource_uuid=resource_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    resource_uuid: UUID,
) -> ResourceApiKeyUsageTotals:
    """Total API key usage of a resource

     Sums the usage the site agent reported for the resource's keys in the current month, per component
    type. Deleted keys are included, so deleting a key leaves the total unchanged.

    Args:
        resource_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyUsageTotals
    """

    return (
        await asyncio_detailed(
            client=client,
            resource_uuid=resource_uuid,
        )
    ).parsed
