from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invoice_item import InvoiceItem
from ...models.invoice_item_o_enum import InvoiceItemOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    conceal_compensation_items: Union[Unset, bool] = UNSET,
    o: Union[Unset, InvoiceItemOEnum] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["conceal_compensation_items"] = conceal_compensation_items

    json_o: Union[Unset, str] = UNSET
    if not isinstance(o, Unset):
        json_o = o.value

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/invoices/{uuid}/items/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> InvoiceItem:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvoiceItem.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[InvoiceItem]:
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
    conceal_compensation_items: Union[Unset, bool] = UNSET,
    o: Union[Unset, InvoiceItemOEnum] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[InvoiceItem]:
    """Get invoice items

     Retrieve a list of invoice items for the specified invoice.

    Args:
        uuid (UUID):
        conceal_compensation_items (Union[Unset, bool]):
        o (Union[Unset, InvoiceItemOEnum]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceItem]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        conceal_compensation_items=conceal_compensation_items,
        o=o,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    conceal_compensation_items: Union[Unset, bool] = UNSET,
    o: Union[Unset, InvoiceItemOEnum] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> InvoiceItem:
    """Get invoice items

     Retrieve a list of invoice items for the specified invoice.

    Args:
        uuid (UUID):
        conceal_compensation_items (Union[Unset, bool]):
        o (Union[Unset, InvoiceItemOEnum]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceItem
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        conceal_compensation_items=conceal_compensation_items,
        o=o,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    conceal_compensation_items: Union[Unset, bool] = UNSET,
    o: Union[Unset, InvoiceItemOEnum] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[InvoiceItem]:
    """Get invoice items

     Retrieve a list of invoice items for the specified invoice.

    Args:
        uuid (UUID):
        conceal_compensation_items (Union[Unset, bool]):
        o (Union[Unset, InvoiceItemOEnum]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceItem]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        conceal_compensation_items=conceal_compensation_items,
        o=o,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    conceal_compensation_items: Union[Unset, bool] = UNSET,
    o: Union[Unset, InvoiceItemOEnum] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> InvoiceItem:
    """Get invoice items

     Retrieve a list of invoice items for the specified invoice.

    Args:
        uuid (UUID):
        conceal_compensation_items (Union[Unset, bool]):
        o (Union[Unset, InvoiceItemOEnum]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceItem
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            conceal_compensation_items=conceal_compensation_items,
            o=o,
            offering_uuid=offering_uuid,
            project_uuid=project_uuid,
            provider_uuid=provider_uuid,
            query=query,
        )
    ).parsed
