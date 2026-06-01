from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.admin_subscription_request import AdminSubscriptionRequest
from ...models.error_response import ErrorResponse
from ...models.subscription_response import SubscriptionResponse
from uuid import UUID


def _get_kwargs(
    account_id: UUID,
    *,
    body: AdminSubscriptionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/accounts/{account_id}/subscription".format(
            account_id=quote(str(account_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SubscriptionResponse | None:
    if response.status_code == 200:
        response_200 = SubscriptionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SubscriptionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AdminSubscriptionRequest,
) -> Response[ErrorResponse | SubscriptionResponse]:
    """Replace Account Subscription (admin)

     Admin replacement of a specific account's subscription.

    Accepts the same body shape as the customer endpoint plus
    ``discount_override_pct``. Setting the override to 100 skips the billing
    provider entirely; lowering it below 100 requires a payment method on
    file for the target account.

    Args:
        account_id (UUID):
        body (AdminSubscriptionRequest): Admin-scope request envelope for replacing a
            subscription.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SubscriptionResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AdminSubscriptionRequest,
) -> ErrorResponse | SubscriptionResponse | None:
    """Replace Account Subscription (admin)

     Admin replacement of a specific account's subscription.

    Accepts the same body shape as the customer endpoint plus
    ``discount_override_pct``. Setting the override to 100 skips the billing
    provider entirely; lowering it below 100 requires a payment method on
    file for the target account.

    Args:
        account_id (UUID):
        body (AdminSubscriptionRequest): Admin-scope request envelope for replacing a
            subscription.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SubscriptionResponse
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AdminSubscriptionRequest,
) -> Response[ErrorResponse | SubscriptionResponse]:
    """Replace Account Subscription (admin)

     Admin replacement of a specific account's subscription.

    Accepts the same body shape as the customer endpoint plus
    ``discount_override_pct``. Setting the override to 100 skips the billing
    provider entirely; lowering it below 100 requires a payment method on
    file for the target account.

    Args:
        account_id (UUID):
        body (AdminSubscriptionRequest): Admin-scope request envelope for replacing a
            subscription.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SubscriptionResponse]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AdminSubscriptionRequest,
) -> ErrorResponse | SubscriptionResponse | None:
    """Replace Account Subscription (admin)

     Admin replacement of a specific account's subscription.

    Accepts the same body shape as the customer endpoint plus
    ``discount_override_pct``. Setting the override to 100 skips the billing
    provider entirely; lowering it below 100 requires a payment method on
    file for the target account.

    Args:
        account_id (UUID):
        body (AdminSubscriptionRequest): Admin-scope request envelope for replacing a
            subscription.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SubscriptionResponse
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            body=body,
        )
    ).parsed
