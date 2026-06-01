from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.flag_bulk_request import FlagBulkRequest
from ...models.flag_bulk_response import FlagBulkResponse


def _get_kwargs(
    *,
    body: FlagBulkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/flags/bulk",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FlagBulkResponse | None:
    if response.status_code == 200:
        response_200 = FlagBulkResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FlagBulkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FlagBulkRequest,
) -> Response[FlagBulkResponse]:
    """Bulk Register Flags

     Register flags discovered by an SDK.

    Creates a new flag for each unreported key and refreshes the
    service/environment source observation on each already-known key.

    Args:
        body (FlagBulkRequest): Inputs to the bulk-register-flags action. Example: {'flags':
            [{'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-
            gateway', 'type': 'BOOLEAN'}, {'default': 3, 'environment': 'production', 'id': 'max-
            retries', 'service': 'api-gateway', 'type': 'NUMERIC'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlagBulkResponse]
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
    body: FlagBulkRequest,
) -> FlagBulkResponse | None:
    """Bulk Register Flags

     Register flags discovered by an SDK.

    Creates a new flag for each unreported key and refreshes the
    service/environment source observation on each already-known key.

    Args:
        body (FlagBulkRequest): Inputs to the bulk-register-flags action. Example: {'flags':
            [{'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-
            gateway', 'type': 'BOOLEAN'}, {'default': 3, 'environment': 'production', 'id': 'max-
            retries', 'service': 'api-gateway', 'type': 'NUMERIC'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlagBulkResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FlagBulkRequest,
) -> Response[FlagBulkResponse]:
    """Bulk Register Flags

     Register flags discovered by an SDK.

    Creates a new flag for each unreported key and refreshes the
    service/environment source observation on each already-known key.

    Args:
        body (FlagBulkRequest): Inputs to the bulk-register-flags action. Example: {'flags':
            [{'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-
            gateway', 'type': 'BOOLEAN'}, {'default': 3, 'environment': 'production', 'id': 'max-
            retries', 'service': 'api-gateway', 'type': 'NUMERIC'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlagBulkResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FlagBulkRequest,
) -> FlagBulkResponse | None:
    """Bulk Register Flags

     Register flags discovered by an SDK.

    Creates a new flag for each unreported key and refreshes the
    service/environment source observation on each already-known key.

    Args:
        body (FlagBulkRequest): Inputs to the bulk-register-flags action. Example: {'flags':
            [{'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-
            gateway', 'type': 'BOOLEAN'}, {'default': 3, 'environment': 'production', 'id': 'max-
            retries', 'service': 'api-gateway', 'type': 'NUMERIC'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlagBulkResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
