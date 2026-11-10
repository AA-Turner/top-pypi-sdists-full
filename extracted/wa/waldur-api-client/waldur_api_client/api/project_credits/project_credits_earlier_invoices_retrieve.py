import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_credit_earlier_invoices import ProjectCreditEarlierInvoices
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    earlier_invoices_from: Union[Unset, datetime.date] = UNSET,
    earlier_invoices_until: Union[Unset, datetime.date] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_earlier_invoices_from: Union[Unset, str] = UNSET
    if not isinstance(earlier_invoices_from, Unset):
        json_earlier_invoices_from = earlier_invoices_from.isoformat()
    params["earlier_invoices_from"] = json_earlier_invoices_from

    json_earlier_invoices_until: Union[Unset, str] = UNSET
    if not isinstance(earlier_invoices_until, Unset):
        json_earlier_invoices_until = earlier_invoices_until.isoformat()
    params["earlier_invoices_until"] = json_earlier_invoices_until

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/project-credits/{uuid}/earlier_invoices/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ProjectCreditEarlierInvoices:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProjectCreditEarlierInvoices.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProjectCreditEarlierInvoices]:
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
    earlier_invoices_from: Union[Unset, datetime.date] = UNSET,
    earlier_invoices_until: Union[Unset, datetime.date] = UNSET,
) -> Response[ProjectCreditEarlierInvoices]:
    """Earlier invoices of the project and what credit paid of them

     Per closed month of the project, the cost the credit could pay and how much of it credit paid,
    either on the month's own invoice or later. This is the cost a period-Total cost policy that takes
    credit into account keeps counting. Every closed month is listed; in_period marks those the credit
    pays, by its earlier_invoices_from / earlier_invoices_until, which can be previewed with other
    bounds.

    Args:
        uuid (UUID):
        earlier_invoices_from (Union[Unset, datetime.date]):
        earlier_invoices_until (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectCreditEarlierInvoices]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        earlier_invoices_from=earlier_invoices_from,
        earlier_invoices_until=earlier_invoices_until,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    earlier_invoices_from: Union[Unset, datetime.date] = UNSET,
    earlier_invoices_until: Union[Unset, datetime.date] = UNSET,
) -> ProjectCreditEarlierInvoices:
    """Earlier invoices of the project and what credit paid of them

     Per closed month of the project, the cost the credit could pay and how much of it credit paid,
    either on the month's own invoice or later. This is the cost a period-Total cost policy that takes
    credit into account keeps counting. Every closed month is listed; in_period marks those the credit
    pays, by its earlier_invoices_from / earlier_invoices_until, which can be previewed with other
    bounds.

    Args:
        uuid (UUID):
        earlier_invoices_from (Union[Unset, datetime.date]):
        earlier_invoices_until (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectCreditEarlierInvoices
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        earlier_invoices_from=earlier_invoices_from,
        earlier_invoices_until=earlier_invoices_until,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    earlier_invoices_from: Union[Unset, datetime.date] = UNSET,
    earlier_invoices_until: Union[Unset, datetime.date] = UNSET,
) -> Response[ProjectCreditEarlierInvoices]:
    """Earlier invoices of the project and what credit paid of them

     Per closed month of the project, the cost the credit could pay and how much of it credit paid,
    either on the month's own invoice or later. This is the cost a period-Total cost policy that takes
    credit into account keeps counting. Every closed month is listed; in_period marks those the credit
    pays, by its earlier_invoices_from / earlier_invoices_until, which can be previewed with other
    bounds.

    Args:
        uuid (UUID):
        earlier_invoices_from (Union[Unset, datetime.date]):
        earlier_invoices_until (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectCreditEarlierInvoices]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        earlier_invoices_from=earlier_invoices_from,
        earlier_invoices_until=earlier_invoices_until,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    earlier_invoices_from: Union[Unset, datetime.date] = UNSET,
    earlier_invoices_until: Union[Unset, datetime.date] = UNSET,
) -> ProjectCreditEarlierInvoices:
    """Earlier invoices of the project and what credit paid of them

     Per closed month of the project, the cost the credit could pay and how much of it credit paid,
    either on the month's own invoice or later. This is the cost a period-Total cost policy that takes
    credit into account keeps counting. Every closed month is listed; in_period marks those the credit
    pays, by its earlier_invoices_from / earlier_invoices_until, which can be previewed with other
    bounds.

    Args:
        uuid (UUID):
        earlier_invoices_from (Union[Unset, datetime.date]):
        earlier_invoices_until (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectCreditEarlierInvoices
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            earlier_invoices_from=earlier_invoices_from,
            earlier_invoices_until=earlier_invoices_until,
        )
    ).parsed
