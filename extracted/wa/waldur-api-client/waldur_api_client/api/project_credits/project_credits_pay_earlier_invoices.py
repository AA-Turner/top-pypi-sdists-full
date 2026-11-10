from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pay_earlier_invoices import PayEarlierInvoices
from ...models.pay_earlier_invoices_request_request import PayEarlierInvoicesRequestRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: PayEarlierInvoicesRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/project-credits/{uuid}/pay_earlier_invoices/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> PayEarlierInvoices:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PayEarlierInvoices.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PayEarlierInvoices]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PayEarlierInvoicesRequestRequest,
) -> Response[PayEarlierInvoices]:
    """Pay earlier invoices from the project credit

     Pays the uncovered cost of the project's earlier, closed invoices from what is left of the credit
    after this month's usage so far, and turns on pay_earlier_invoices so that each month end pays more.
    With dry_run, returns the compensations it would write and the balances before and after, and
    changes nothing.

    Args:
        uuid (UUID):
        body (PayEarlierInvoicesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PayEarlierInvoices]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PayEarlierInvoicesRequestRequest,
) -> PayEarlierInvoices:
    """Pay earlier invoices from the project credit

     Pays the uncovered cost of the project's earlier, closed invoices from what is left of the credit
    after this month's usage so far, and turns on pay_earlier_invoices so that each month end pays more.
    With dry_run, returns the compensations it would write and the balances before and after, and
    changes nothing.

    Args:
        uuid (UUID):
        body (PayEarlierInvoicesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PayEarlierInvoices
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PayEarlierInvoicesRequestRequest,
) -> Response[PayEarlierInvoices]:
    """Pay earlier invoices from the project credit

     Pays the uncovered cost of the project's earlier, closed invoices from what is left of the credit
    after this month's usage so far, and turns on pay_earlier_invoices so that each month end pays more.
    With dry_run, returns the compensations it would write and the balances before and after, and
    changes nothing.

    Args:
        uuid (UUID):
        body (PayEarlierInvoicesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PayEarlierInvoices]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PayEarlierInvoicesRequestRequest,
) -> PayEarlierInvoices:
    """Pay earlier invoices from the project credit

     Pays the uncovered cost of the project's earlier, closed invoices from what is left of the credit
    after this month's usage so far, and turns on pay_earlier_invoices so that each month end pays more.
    With dry_run, returns the compensations it would write and the balances before and after, and
    changes nothing.

    Args:
        uuid (UUID):
        body (PayEarlierInvoicesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PayEarlierInvoices
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
