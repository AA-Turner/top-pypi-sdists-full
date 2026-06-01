from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.invoice_single_response import InvoiceSingleResponse


def _get_kwargs(
    invoice_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/invoices/{invoice_id}".format(
            invoice_id=quote(str(invoice_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | InvoiceSingleResponse | None:
    if response.status_code == 200:
        response_200 = InvoiceSingleResponse.from_dict(response.json())

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

    if response.status_code == 406:
        response_406 = ErrorResponse.from_dict(response.json())

        return response_406

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | InvoiceSingleResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invoice_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | InvoiceSingleResponse]:
    """Get Invoice

     Return a single invoice by id. Supports content negotiation via the
    `Accept` header:

    - `application/pdf` — streams the invoice PDF.
    - `application/vnd.api+json`, `application/json`, or absent — returns
      the JSON:API invoice resource.
    - Any other value — `406 Not Acceptable`.

    Args:
        invoice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvoiceSingleResponse]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invoice_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | InvoiceSingleResponse | None:
    """Get Invoice

     Return a single invoice by id. Supports content negotiation via the
    `Accept` header:

    - `application/pdf` — streams the invoice PDF.
    - `application/vnd.api+json`, `application/json`, or absent — returns
      the JSON:API invoice resource.
    - Any other value — `406 Not Acceptable`.

    Args:
        invoice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvoiceSingleResponse
    """

    return sync_detailed(
        invoice_id=invoice_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    invoice_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | InvoiceSingleResponse]:
    """Get Invoice

     Return a single invoice by id. Supports content negotiation via the
    `Accept` header:

    - `application/pdf` — streams the invoice PDF.
    - `application/vnd.api+json`, `application/json`, or absent — returns
      the JSON:API invoice resource.
    - Any other value — `406 Not Acceptable`.

    Args:
        invoice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvoiceSingleResponse]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invoice_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | InvoiceSingleResponse | None:
    """Get Invoice

     Return a single invoice by id. Supports content negotiation via the
    `Accept` header:

    - `application/pdf` — streams the invoice PDF.
    - `application/vnd.api+json`, `application/json`, or absent — returns
      the JSON:API invoice resource.
    - Any other value — `406 Not Acceptable`.

    Args:
        invoice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvoiceSingleResponse
    """

    return (
        await asyncio_detailed(
            invoice_id=invoice_id,
            client=client,
        )
    ).parsed
