from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.customer_service_account import CustomerServiceAccount
from ...models.customer_service_account_request import CustomerServiceAccountRequest
from ...types import Response


def _get_kwargs(
    *,
    body: CustomerServiceAccountRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-customer-service-accounts/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CustomerServiceAccount:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = CustomerServiceAccount.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CustomerServiceAccount]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CustomerServiceAccountRequest,
) -> Response[CustomerServiceAccount]:
    """Create a customer service account

     Creates a new service account scoped to a specific customer (organization). This generates an API
    key that can be used for automated access to resources across all projects within that customer.

    Args:
        body (CustomerServiceAccountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomerServiceAccount]
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
    body: CustomerServiceAccountRequest,
) -> CustomerServiceAccount:
    """Create a customer service account

     Creates a new service account scoped to a specific customer (organization). This generates an API
    key that can be used for automated access to resources across all projects within that customer.

    Args:
        body (CustomerServiceAccountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomerServiceAccount
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CustomerServiceAccountRequest,
) -> Response[CustomerServiceAccount]:
    """Create a customer service account

     Creates a new service account scoped to a specific customer (organization). This generates an API
    key that can be used for automated access to resources across all projects within that customer.

    Args:
        body (CustomerServiceAccountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomerServiceAccount]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CustomerServiceAccountRequest,
) -> CustomerServiceAccount:
    """Create a customer service account

     Creates a new service account scoped to a specific customer (organization). This generates an API
    key that can be used for automated access to resources across all projects within that customer.

    Args:
        body (CustomerServiceAccountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomerServiceAccount
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
