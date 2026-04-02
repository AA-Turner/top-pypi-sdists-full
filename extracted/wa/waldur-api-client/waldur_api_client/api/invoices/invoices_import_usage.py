from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.import_usage_request import ImportUsageRequest
from ...models.import_usage_response import ImportUsageResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ImportUsageRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/invoices/import_usage/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ImportUsageResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ImportUsageResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ImportUsageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportUsageRequest,
) -> Response[ImportUsageResponse]:
    """Import usage data

     Import component usage items as JSON data for multiple customers. Creates invoice items for the
    specified billing period. Items are deduplicated by name, customer, and billing period to prevent
    duplicates.

    Args:
        body (ImportUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImportUsageResponse]
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
    body: ImportUsageRequest,
) -> ImportUsageResponse:
    """Import usage data

     Import component usage items as JSON data for multiple customers. Creates invoice items for the
    specified billing period. Items are deduplicated by name, customer, and billing period to prevent
    duplicates.

    Args:
        body (ImportUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImportUsageResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportUsageRequest,
) -> Response[ImportUsageResponse]:
    """Import usage data

     Import component usage items as JSON data for multiple customers. Creates invoice items for the
    specified billing period. Items are deduplicated by name, customer, and billing period to prevent
    duplicates.

    Args:
        body (ImportUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImportUsageResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ImportUsageRequest,
) -> ImportUsageResponse:
    """Import usage data

     Import component usage items as JSON data for multiple customers. Creates invoice items for the
    specified billing period. Items are deduplicated by name, customer, and billing period to prevent
    duplicates.

    Args:
        body (ImportUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImportUsageResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
