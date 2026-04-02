from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    abbreviation: Union[Unset, str] = UNSET,
    accounting_is_running: Union[Unset, bool] = UNSET,
    agreement_number: Union[Unset, str] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    contact_details: Union[Unset, str] = UNSET,
    current_user_has_project_create_permission: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization_group_name: Union[Unset, str] = UNSET,
    organization_group_uuid: Union[Unset, list[UUID]] = UNSET,
    owned_by_current_user: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["abbreviation"] = abbreviation

    params["accounting_is_running"] = accounting_is_running

    params["agreement_number"] = agreement_number

    params["archived"] = archived

    params["backend_id"] = backend_id

    params["contact_details"] = contact_details

    params["current_user_has_project_create_permission"] = current_user_has_project_create_permission

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["month"] = month

    params["name"] = name

    params["name_exact"] = name_exact

    params["native_name"] = native_name

    params["o"] = o

    params["organization_group_name"] = organization_group_name

    json_organization_group_uuid: Union[Unset, list[str]] = UNSET
    if not isinstance(organization_group_uuid, Unset):
        json_organization_group_uuid = []
        for organization_group_uuid_item_data in organization_group_uuid:
            organization_group_uuid_item = str(organization_group_uuid_item_data)
            json_organization_group_uuid.append(organization_group_uuid_item)

    params["organization_group_uuid"] = json_organization_group_uuid

    params["owned_by_current_user"] = owned_by_current_user

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    params["registration_code"] = registration_code

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/financial-reports/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    accounting_is_running: Union[Unset, bool] = UNSET,
    agreement_number: Union[Unset, str] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    contact_details: Union[Unset, str] = UNSET,
    current_user_has_project_create_permission: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization_group_name: Union[Unset, str] = UNSET,
    organization_group_uuid: Union[Unset, list[UUID]] = UNSET,
    owned_by_current_user: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        abbreviation (Union[Unset, str]):
        accounting_is_running (Union[Unset, bool]):
        agreement_number (Union[Unset, str]):
        archived (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        contact_details (Union[Unset, str]):
        current_user_has_project_create_permission (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, str]):
        organization_group_name (Union[Unset, str]):
        organization_group_uuid (Union[Unset, list[UUID]]):
        owned_by_current_user (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        accounting_is_running=accounting_is_running,
        agreement_number=agreement_number,
        archived=archived,
        backend_id=backend_id,
        contact_details=contact_details,
        current_user_has_project_create_permission=current_user_has_project_create_permission,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        name_exact=name_exact,
        native_name=native_name,
        o=o,
        organization_group_name=organization_group_name,
        organization_group_uuid=organization_group_uuid,
        owned_by_current_user=owned_by_current_user,
        page=page,
        page_size=page_size,
        query=query,
        registration_code=registration_code,
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    accounting_is_running: Union[Unset, bool] = UNSET,
    agreement_number: Union[Unset, str] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    contact_details: Union[Unset, str] = UNSET,
    current_user_has_project_create_permission: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization_group_name: Union[Unset, str] = UNSET,
    organization_group_uuid: Union[Unset, list[UUID]] = UNSET,
    owned_by_current_user: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        abbreviation (Union[Unset, str]):
        accounting_is_running (Union[Unset, bool]):
        agreement_number (Union[Unset, str]):
        archived (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        contact_details (Union[Unset, str]):
        current_user_has_project_create_permission (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, str]):
        organization_group_name (Union[Unset, str]):
        organization_group_uuid (Union[Unset, list[UUID]]):
        owned_by_current_user (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        abbreviation=abbreviation,
        accounting_is_running=accounting_is_running,
        agreement_number=agreement_number,
        archived=archived,
        backend_id=backend_id,
        contact_details=contact_details,
        current_user_has_project_create_permission=current_user_has_project_create_permission,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        name_exact=name_exact,
        native_name=native_name,
        o=o,
        organization_group_name=organization_group_name,
        organization_group_uuid=organization_group_uuid,
        owned_by_current_user=owned_by_current_user,
        page=page,
        page_size=page_size,
        query=query,
        registration_code=registration_code,
        year=year,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    accounting_is_running: Union[Unset, bool] = UNSET,
    agreement_number: Union[Unset, str] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    contact_details: Union[Unset, str] = UNSET,
    current_user_has_project_create_permission: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization_group_name: Union[Unset, str] = UNSET,
    organization_group_uuid: Union[Unset, list[UUID]] = UNSET,
    owned_by_current_user: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        abbreviation (Union[Unset, str]):
        accounting_is_running (Union[Unset, bool]):
        agreement_number (Union[Unset, str]):
        archived (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        contact_details (Union[Unset, str]):
        current_user_has_project_create_permission (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, str]):
        organization_group_name (Union[Unset, str]):
        organization_group_uuid (Union[Unset, list[UUID]]):
        owned_by_current_user (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        accounting_is_running=accounting_is_running,
        agreement_number=agreement_number,
        archived=archived,
        backend_id=backend_id,
        contact_details=contact_details,
        current_user_has_project_create_permission=current_user_has_project_create_permission,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        name_exact=name_exact,
        native_name=native_name,
        o=o,
        organization_group_name=organization_group_name,
        organization_group_uuid=organization_group_uuid,
        owned_by_current_user=owned_by_current_user,
        page=page,
        page_size=page_size,
        query=query,
        registration_code=registration_code,
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    accounting_is_running: Union[Unset, bool] = UNSET,
    agreement_number: Union[Unset, str] = UNSET,
    archived: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    contact_details: Union[Unset, str] = UNSET,
    current_user_has_project_create_permission: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization_group_name: Union[Unset, str] = UNSET,
    organization_group_uuid: Union[Unset, list[UUID]] = UNSET,
    owned_by_current_user: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        abbreviation (Union[Unset, str]):
        accounting_is_running (Union[Unset, bool]):
        agreement_number (Union[Unset, str]):
        archived (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        contact_details (Union[Unset, str]):
        current_user_has_project_create_permission (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, str]):
        organization_group_name (Union[Unset, str]):
        organization_group_uuid (Union[Unset, list[UUID]]):
        owned_by_current_user (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            abbreviation=abbreviation,
            accounting_is_running=accounting_is_running,
            agreement_number=agreement_number,
            archived=archived,
            backend_id=backend_id,
            contact_details=contact_details,
            current_user_has_project_create_permission=current_user_has_project_create_permission,
            customer_uuid=customer_uuid,
            month=month,
            name=name,
            name_exact=name_exact,
            native_name=native_name,
            o=o,
            organization_group_name=organization_group_name,
            organization_group_uuid=organization_group_uuid,
            owned_by_current_user=owned_by_current_user,
            page=page,
            page_size=page_size,
            query=query,
            registration_code=registration_code,
            year=year,
        )
    ).parsed
