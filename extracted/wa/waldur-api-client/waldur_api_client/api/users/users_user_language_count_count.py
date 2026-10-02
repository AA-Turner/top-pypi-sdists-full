import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_service_provider_user_o_enum import MarketplaceServiceProviderUserOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_staff: Union[Unset, bool] = UNSET,
    is_support: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceServiceProviderUserOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_roles: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    project_roles: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    username_list: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_agreement_date: Union[Unset, str] = UNSET
    if not isinstance(agreement_date, Unset):
        json_agreement_date = agreement_date.isoformat()
    params["agreement_date"] = json_agreement_date

    params["civil_number"] = civil_number

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_date_joined: Union[Unset, str] = UNSET
    if not isinstance(date_joined, Unset):
        json_date_joined = date_joined.isoformat()
    params["date_joined"] = json_date_joined

    params["description"] = description

    params["email"] = email

    params["full_name"] = full_name

    params["is_active"] = is_active

    params["is_staff"] = is_staff

    params["is_support"] = is_support

    params["job_title"] = job_title

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["native_name"] = native_name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["organization"] = organization

    params["organization_roles"] = organization_roles

    params["page"] = page

    params["page_size"] = page_size

    params["phone_number"] = phone_number

    params["project_roles"] = project_roles

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["query"] = query

    params["registration_method"] = registration_method

    params["user_keyword"] = user_keyword

    params["username"] = username

    params["username_list"] = username_list

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/users/user_language_count/",
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
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_staff: Union[Unset, bool] = UNSET,
    is_support: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceServiceProviderUserOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_roles: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    project_roles: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    username_list: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get user counts by preferred language

     Get number of items in the collection matching the request parameters.

    Args:
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        is_staff (Union[Unset, bool]):
        is_support (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceServiceProviderUserOEnum]]):
        organization (Union[Unset, str]):
        organization_roles (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        project_roles (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):
        username_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        agreement_date=agreement_date,
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        is_staff=is_staff,
        is_support=is_support,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        organization_roles=organization_roles,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        project_roles=project_roles,
        project_uuid=project_uuid,
        query=query,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
        username_list=username_list,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_staff: Union[Unset, bool] = UNSET,
    is_support: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceServiceProviderUserOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_roles: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    project_roles: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    username_list: Union[Unset, str] = UNSET,
) -> int:
    """Get user counts by preferred language

     Get number of items in the collection matching the request parameters.

    Args:
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        is_staff (Union[Unset, bool]):
        is_support (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceServiceProviderUserOEnum]]):
        organization (Union[Unset, str]):
        organization_roles (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        project_roles (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):
        username_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        agreement_date=agreement_date,
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        is_staff=is_staff,
        is_support=is_support,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        organization_roles=organization_roles,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        project_roles=project_roles,
        project_uuid=project_uuid,
        query=query,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
        username_list=username_list,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_staff: Union[Unset, bool] = UNSET,
    is_support: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceServiceProviderUserOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_roles: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    project_roles: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    username_list: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get user counts by preferred language

     Get number of items in the collection matching the request parameters.

    Args:
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        is_staff (Union[Unset, bool]):
        is_support (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceServiceProviderUserOEnum]]):
        organization (Union[Unset, str]):
        organization_roles (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        project_roles (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):
        username_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        agreement_date=agreement_date,
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        date_joined=date_joined,
        description=description,
        email=email,
        full_name=full_name,
        is_active=is_active,
        is_staff=is_staff,
        is_support=is_support,
        job_title=job_title,
        modified=modified,
        native_name=native_name,
        o=o,
        organization=organization,
        organization_roles=organization_roles,
        page=page,
        page_size=page_size,
        phone_number=phone_number,
        project_roles=project_roles,
        project_uuid=project_uuid,
        query=query,
        registration_method=registration_method,
        user_keyword=user_keyword,
        username=username,
        username_list=username_list,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    agreement_date: Union[Unset, datetime.datetime] = UNSET,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_joined: Union[Unset, datetime.datetime] = UNSET,
    description: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_staff: Union[Unset, bool] = UNSET,
    is_support: Union[Unset, bool] = UNSET,
    job_title: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceServiceProviderUserOEnum]] = UNSET,
    organization: Union[Unset, str] = UNSET,
    organization_roles: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    phone_number: Union[Unset, str] = UNSET,
    project_roles: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    registration_method: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    username_list: Union[Unset, str] = UNSET,
) -> int:
    """Get user counts by preferred language

     Get number of items in the collection matching the request parameters.

    Args:
        agreement_date (Union[Unset, datetime.datetime]):
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        date_joined (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        full_name (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        is_staff (Union[Unset, bool]):
        is_support (Union[Unset, bool]):
        job_title (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceServiceProviderUserOEnum]]):
        organization (Union[Unset, str]):
        organization_roles (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        phone_number (Union[Unset, str]):
        project_roles (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        registration_method (Union[Unset, str]):
        user_keyword (Union[Unset, str]):
        username (Union[Unset, str]):
        username_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            agreement_date=agreement_date,
            civil_number=civil_number,
            customer_uuid=customer_uuid,
            date_joined=date_joined,
            description=description,
            email=email,
            full_name=full_name,
            is_active=is_active,
            is_staff=is_staff,
            is_support=is_support,
            job_title=job_title,
            modified=modified,
            native_name=native_name,
            o=o,
            organization=organization,
            organization_roles=organization_roles,
            page=page,
            page_size=page_size,
            phone_number=phone_number,
            project_roles=project_roles,
            project_uuid=project_uuid,
            query=query,
            registration_method=registration_method,
            user_keyword=user_keyword,
            username=username,
            username_list=username_list,
        )
    ).parsed
