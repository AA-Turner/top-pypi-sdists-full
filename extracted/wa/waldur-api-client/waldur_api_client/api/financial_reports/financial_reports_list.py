from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.financial_report import FinancialReport
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/financial-reports/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["FinancialReport"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FinancialReport.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["FinancialReport"]]:
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
) -> Response[list["FinancialReport"]]:
    """
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
        Response[list['FinancialReport']]
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
) -> list["FinancialReport"]:
    """
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
        list['FinancialReport']
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
) -> Response[list["FinancialReport"]]:
    """
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
        Response[list['FinancialReport']]
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
) -> list["FinancialReport"]:
    """
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
        list['FinancialReport']
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


def sync_all(
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
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["FinancialReport"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

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
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FinancialReport']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[FinancialReport] = []

    # Get initial request kwargs
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
        query=query,
        registration_code=registration_code,
        year=year,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
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
    query: Union[Unset, str] = UNSET,
    registration_code: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["FinancialReport"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

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
        query (Union[Unset, str]):
        registration_code (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FinancialReport']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[FinancialReport] = []

    # Get initial request kwargs
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
        query=query,
        registration_code=registration_code,
        year=year,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
