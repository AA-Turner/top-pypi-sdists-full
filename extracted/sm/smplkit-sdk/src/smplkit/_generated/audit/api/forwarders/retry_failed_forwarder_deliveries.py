from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.retry_failed_deliveries_summary import RetryFailedDeliveriesSummary


def _get_kwargs(
    forwarder_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/forwarders/{forwarder_id}/actions/retry_failed_deliveries".format(
            forwarder_id=quote(str(forwarder_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RetryFailedDeliveriesSummary | None:
    if response.status_code == 200:
        response_200 = RetryFailedDeliveriesSummary.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RetryFailedDeliveriesSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RetryFailedDeliveriesSummary]:
    """Retry Failed Forwarder Deliveries

     Retry every failed delivery for this forwarder in the resolved environment.

    Scoped to the resolved environment (a single-environment credential
    implies it; otherwise send the `X-Smplkit-Environment` header): only
    that environment's failed deliveries are re-attempted, each using the
    forwarder's effective configuration for that environment and the
    original event. Returns the counts.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RetryFailedDeliveriesSummary]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> RetryFailedDeliveriesSummary | None:
    """Retry Failed Forwarder Deliveries

     Retry every failed delivery for this forwarder in the resolved environment.

    Scoped to the resolved environment (a single-environment credential
    implies it; otherwise send the `X-Smplkit-Environment` header): only
    that environment's failed deliveries are re-attempted, each using the
    forwarder's effective configuration for that environment and the
    original event. Returns the counts.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RetryFailedDeliveriesSummary
    """

    return sync_detailed(
        forwarder_id=forwarder_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RetryFailedDeliveriesSummary]:
    """Retry Failed Forwarder Deliveries

     Retry every failed delivery for this forwarder in the resolved environment.

    Scoped to the resolved environment (a single-environment credential
    implies it; otherwise send the `X-Smplkit-Environment` header): only
    that environment's failed deliveries are re-attempted, each using the
    forwarder's effective configuration for that environment and the
    original event. Returns the counts.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RetryFailedDeliveriesSummary]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> RetryFailedDeliveriesSummary | None:
    """Retry Failed Forwarder Deliveries

     Retry every failed delivery for this forwarder in the resolved environment.

    Scoped to the resolved environment (a single-environment credential
    implies it; otherwise send the `X-Smplkit-Environment` header): only
    that environment's failed deliveries are re-attempted, each using the
    forwarder's effective configuration for that environment and the
    original event. Returns the counts.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RetryFailedDeliveriesSummary
    """

    return (
        await asyncio_detailed(
            forwarder_id=forwarder_id,
            client=client,
        )
    ).parsed
