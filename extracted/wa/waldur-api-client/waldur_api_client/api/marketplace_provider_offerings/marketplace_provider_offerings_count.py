import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_state import OfferingState
from ...models.provider_offering_details_o_enum import ProviderOfferingDetailsOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    accessible_via_calls: Union[Unset, bool] = UNSET,
    allowed_customer_uuid: Union[Unset, UUID] = UNSET,
    attributes: Union[Unset, str] = UNSET,
    billable: Union[Unset, bool] = UNSET,
    can_create_offering_user: Union[Unset, bool] = UNSET,
    category_group_uuid: Union[Unset, UUID] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_active_terms_of_service: Union[Unset, bool] = UNSET,
    has_terms_of_service: Union[Unset, bool] = UNSET,
    importable: Union[Unset, str] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProviderOfferingDetailsOEnum]] = UNSET,
    organization_group_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[OfferingState]] = UNSET,
    tag: Union[Unset, list[UUID]] = UNSET,
    tag_name: Union[Unset, list[str]] = UNSET,
    tag_names_and: Union[Unset, str] = UNSET,
    tags_and: Union[Unset, str] = UNSET,
    type_: Union[Unset, list[str]] = UNSET,
    user_has_consent: Union[Unset, bool] = UNSET,
    user_has_offering_user: Union[Unset, bool] = UNSET,
    uuid_list: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accessible_via_calls"] = accessible_via_calls

    json_allowed_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(allowed_customer_uuid, Unset):
        json_allowed_customer_uuid = str(allowed_customer_uuid)
    params["allowed_customer_uuid"] = json_allowed_customer_uuid

    params["attributes"] = attributes

    params["billable"] = billable

    params["can_create_offering_user"] = can_create_offering_user

    json_category_group_uuid: Union[Unset, str] = UNSET
    if not isinstance(category_group_uuid, Unset):
        json_category_group_uuid = str(category_group_uuid)
    params["category_group_uuid"] = json_category_group_uuid

    json_category_uuid: Union[Unset, str] = UNSET
    if not isinstance(category_uuid, Unset):
        json_category_uuid = str(category_uuid)
    params["category_uuid"] = json_category_uuid

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    params["customer"] = customer

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["description"] = description

    params["has_active_terms_of_service"] = has_active_terms_of_service

    params["has_terms_of_service"] = has_terms_of_service

    params["importable"] = importable

    params["keyword"] = keyword

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["name"] = name

    params["name_exact"] = name_exact

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_organization_group_uuid: Union[Unset, str] = UNSET
    if not isinstance(organization_group_uuid, Unset):
        json_organization_group_uuid = str(organization_group_uuid)
    params["organization_group_uuid"] = json_organization_group_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_parent_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_uuid, Unset):
        json_parent_uuid = str(parent_uuid)
    params["parent_uuid"] = json_parent_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["query"] = query

    json_resource_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_customer_uuid, Unset):
        json_resource_customer_uuid = str(resource_customer_uuid)
    params["resource_customer_uuid"] = json_resource_customer_uuid

    json_resource_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_project_uuid, Unset):
        json_resource_project_uuid = str(resource_project_uuid)
    params["resource_project_uuid"] = json_resource_project_uuid

    params["scope_uuid"] = scope_uuid

    json_service_manager_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_manager_uuid, Unset):
        json_service_manager_uuid = str(service_manager_uuid)
    params["service_manager_uuid"] = json_service_manager_uuid

    params["shared"] = shared

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_tag: Union[Unset, list[str]] = UNSET
    if not isinstance(tag, Unset):
        json_tag = []
        for tag_item_data in tag:
            tag_item = str(tag_item_data)
            json_tag.append(tag_item)

    params["tag"] = json_tag

    json_tag_name: Union[Unset, list[str]] = UNSET
    if not isinstance(tag_name, Unset):
        json_tag_name = tag_name

    params["tag_name"] = json_tag_name

    params["tag_names_and"] = tag_names_and

    params["tags_and"] = tags_and

    json_type_: Union[Unset, list[str]] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_

    params["type"] = json_type_

    params["user_has_consent"] = user_has_consent

    params["user_has_offering_user"] = user_has_offering_user

    params["uuid_list"] = uuid_list

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-provider-offerings/",
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
    accessible_via_calls: Union[Unset, bool] = UNSET,
    allowed_customer_uuid: Union[Unset, UUID] = UNSET,
    attributes: Union[Unset, str] = UNSET,
    billable: Union[Unset, bool] = UNSET,
    can_create_offering_user: Union[Unset, bool] = UNSET,
    category_group_uuid: Union[Unset, UUID] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_active_terms_of_service: Union[Unset, bool] = UNSET,
    has_terms_of_service: Union[Unset, bool] = UNSET,
    importable: Union[Unset, str] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProviderOfferingDetailsOEnum]] = UNSET,
    organization_group_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[OfferingState]] = UNSET,
    tag: Union[Unset, list[UUID]] = UNSET,
    tag_name: Union[Unset, list[str]] = UNSET,
    tag_names_and: Union[Unset, str] = UNSET,
    tags_and: Union[Unset, str] = UNSET,
    type_: Union[Unset, list[str]] = UNSET,
    user_has_consent: Union[Unset, bool] = UNSET,
    user_has_offering_user: Union[Unset, bool] = UNSET,
    uuid_list: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List provider offerings

     Get number of items in the collection matching the request parameters.

    Args:
        accessible_via_calls (Union[Unset, bool]):
        allowed_customer_uuid (Union[Unset, UUID]):
        attributes (Union[Unset, str]):
        billable (Union[Unset, bool]):
        can_create_offering_user (Union[Unset, bool]):
        category_group_uuid (Union[Unset, UUID]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        has_active_terms_of_service (Union[Unset, bool]):
        has_terms_of_service (Union[Unset, bool]):
        importable (Union[Unset, str]):
        keyword (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ProviderOfferingDetailsOEnum]]):
        organization_group_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        scope_uuid (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):
        state (Union[Unset, list[OfferingState]]):
        tag (Union[Unset, list[UUID]]):
        tag_name (Union[Unset, list[str]]):
        tag_names_and (Union[Unset, str]):
        tags_and (Union[Unset, str]):
        type_ (Union[Unset, list[str]]):
        user_has_consent (Union[Unset, bool]):
        user_has_offering_user (Union[Unset, bool]):
        uuid_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        accessible_via_calls=accessible_via_calls,
        allowed_customer_uuid=allowed_customer_uuid,
        attributes=attributes,
        billable=billable,
        can_create_offering_user=can_create_offering_user,
        category_group_uuid=category_group_uuid,
        category_uuid=category_uuid,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        has_active_terms_of_service=has_active_terms_of_service,
        has_terms_of_service=has_terms_of_service,
        importable=importable,
        keyword=keyword,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        organization_group_uuid=organization_group_uuid,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
        project_uuid=project_uuid,
        query=query,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        scope_uuid=scope_uuid,
        service_manager_uuid=service_manager_uuid,
        shared=shared,
        state=state,
        tag=tag,
        tag_name=tag_name,
        tag_names_and=tag_names_and,
        tags_and=tags_and,
        type_=type_,
        user_has_consent=user_has_consent,
        user_has_offering_user=user_has_offering_user,
        uuid_list=uuid_list,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    accessible_via_calls: Union[Unset, bool] = UNSET,
    allowed_customer_uuid: Union[Unset, UUID] = UNSET,
    attributes: Union[Unset, str] = UNSET,
    billable: Union[Unset, bool] = UNSET,
    can_create_offering_user: Union[Unset, bool] = UNSET,
    category_group_uuid: Union[Unset, UUID] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_active_terms_of_service: Union[Unset, bool] = UNSET,
    has_terms_of_service: Union[Unset, bool] = UNSET,
    importable: Union[Unset, str] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProviderOfferingDetailsOEnum]] = UNSET,
    organization_group_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[OfferingState]] = UNSET,
    tag: Union[Unset, list[UUID]] = UNSET,
    tag_name: Union[Unset, list[str]] = UNSET,
    tag_names_and: Union[Unset, str] = UNSET,
    tags_and: Union[Unset, str] = UNSET,
    type_: Union[Unset, list[str]] = UNSET,
    user_has_consent: Union[Unset, bool] = UNSET,
    user_has_offering_user: Union[Unset, bool] = UNSET,
    uuid_list: Union[Unset, str] = UNSET,
) -> int:
    """List provider offerings

     Get number of items in the collection matching the request parameters.

    Args:
        accessible_via_calls (Union[Unset, bool]):
        allowed_customer_uuid (Union[Unset, UUID]):
        attributes (Union[Unset, str]):
        billable (Union[Unset, bool]):
        can_create_offering_user (Union[Unset, bool]):
        category_group_uuid (Union[Unset, UUID]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        has_active_terms_of_service (Union[Unset, bool]):
        has_terms_of_service (Union[Unset, bool]):
        importable (Union[Unset, str]):
        keyword (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ProviderOfferingDetailsOEnum]]):
        organization_group_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        scope_uuid (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):
        state (Union[Unset, list[OfferingState]]):
        tag (Union[Unset, list[UUID]]):
        tag_name (Union[Unset, list[str]]):
        tag_names_and (Union[Unset, str]):
        tags_and (Union[Unset, str]):
        type_ (Union[Unset, list[str]]):
        user_has_consent (Union[Unset, bool]):
        user_has_offering_user (Union[Unset, bool]):
        uuid_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        accessible_via_calls=accessible_via_calls,
        allowed_customer_uuid=allowed_customer_uuid,
        attributes=attributes,
        billable=billable,
        can_create_offering_user=can_create_offering_user,
        category_group_uuid=category_group_uuid,
        category_uuid=category_uuid,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        has_active_terms_of_service=has_active_terms_of_service,
        has_terms_of_service=has_terms_of_service,
        importable=importable,
        keyword=keyword,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        organization_group_uuid=organization_group_uuid,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
        project_uuid=project_uuid,
        query=query,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        scope_uuid=scope_uuid,
        service_manager_uuid=service_manager_uuid,
        shared=shared,
        state=state,
        tag=tag,
        tag_name=tag_name,
        tag_names_and=tag_names_and,
        tags_and=tags_and,
        type_=type_,
        user_has_consent=user_has_consent,
        user_has_offering_user=user_has_offering_user,
        uuid_list=uuid_list,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    accessible_via_calls: Union[Unset, bool] = UNSET,
    allowed_customer_uuid: Union[Unset, UUID] = UNSET,
    attributes: Union[Unset, str] = UNSET,
    billable: Union[Unset, bool] = UNSET,
    can_create_offering_user: Union[Unset, bool] = UNSET,
    category_group_uuid: Union[Unset, UUID] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_active_terms_of_service: Union[Unset, bool] = UNSET,
    has_terms_of_service: Union[Unset, bool] = UNSET,
    importable: Union[Unset, str] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProviderOfferingDetailsOEnum]] = UNSET,
    organization_group_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[OfferingState]] = UNSET,
    tag: Union[Unset, list[UUID]] = UNSET,
    tag_name: Union[Unset, list[str]] = UNSET,
    tag_names_and: Union[Unset, str] = UNSET,
    tags_and: Union[Unset, str] = UNSET,
    type_: Union[Unset, list[str]] = UNSET,
    user_has_consent: Union[Unset, bool] = UNSET,
    user_has_offering_user: Union[Unset, bool] = UNSET,
    uuid_list: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List provider offerings

     Get number of items in the collection matching the request parameters.

    Args:
        accessible_via_calls (Union[Unset, bool]):
        allowed_customer_uuid (Union[Unset, UUID]):
        attributes (Union[Unset, str]):
        billable (Union[Unset, bool]):
        can_create_offering_user (Union[Unset, bool]):
        category_group_uuid (Union[Unset, UUID]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        has_active_terms_of_service (Union[Unset, bool]):
        has_terms_of_service (Union[Unset, bool]):
        importable (Union[Unset, str]):
        keyword (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ProviderOfferingDetailsOEnum]]):
        organization_group_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        scope_uuid (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):
        state (Union[Unset, list[OfferingState]]):
        tag (Union[Unset, list[UUID]]):
        tag_name (Union[Unset, list[str]]):
        tag_names_and (Union[Unset, str]):
        tags_and (Union[Unset, str]):
        type_ (Union[Unset, list[str]]):
        user_has_consent (Union[Unset, bool]):
        user_has_offering_user (Union[Unset, bool]):
        uuid_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        accessible_via_calls=accessible_via_calls,
        allowed_customer_uuid=allowed_customer_uuid,
        attributes=attributes,
        billable=billable,
        can_create_offering_user=can_create_offering_user,
        category_group_uuid=category_group_uuid,
        category_uuid=category_uuid,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        has_active_terms_of_service=has_active_terms_of_service,
        has_terms_of_service=has_terms_of_service,
        importable=importable,
        keyword=keyword,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        organization_group_uuid=organization_group_uuid,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
        project_uuid=project_uuid,
        query=query,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        scope_uuid=scope_uuid,
        service_manager_uuid=service_manager_uuid,
        shared=shared,
        state=state,
        tag=tag,
        tag_name=tag_name,
        tag_names_and=tag_names_and,
        tags_and=tags_and,
        type_=type_,
        user_has_consent=user_has_consent,
        user_has_offering_user=user_has_offering_user,
        uuid_list=uuid_list,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    accessible_via_calls: Union[Unset, bool] = UNSET,
    allowed_customer_uuid: Union[Unset, UUID] = UNSET,
    attributes: Union[Unset, str] = UNSET,
    billable: Union[Unset, bool] = UNSET,
    can_create_offering_user: Union[Unset, bool] = UNSET,
    category_group_uuid: Union[Unset, UUID] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_active_terms_of_service: Union[Unset, bool] = UNSET,
    has_terms_of_service: Union[Unset, bool] = UNSET,
    importable: Union[Unset, str] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProviderOfferingDetailsOEnum]] = UNSET,
    organization_group_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[OfferingState]] = UNSET,
    tag: Union[Unset, list[UUID]] = UNSET,
    tag_name: Union[Unset, list[str]] = UNSET,
    tag_names_and: Union[Unset, str] = UNSET,
    tags_and: Union[Unset, str] = UNSET,
    type_: Union[Unset, list[str]] = UNSET,
    user_has_consent: Union[Unset, bool] = UNSET,
    user_has_offering_user: Union[Unset, bool] = UNSET,
    uuid_list: Union[Unset, str] = UNSET,
) -> int:
    """List provider offerings

     Get number of items in the collection matching the request parameters.

    Args:
        accessible_via_calls (Union[Unset, bool]):
        allowed_customer_uuid (Union[Unset, UUID]):
        attributes (Union[Unset, str]):
        billable (Union[Unset, bool]):
        can_create_offering_user (Union[Unset, bool]):
        category_group_uuid (Union[Unset, UUID]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        has_active_terms_of_service (Union[Unset, bool]):
        has_terms_of_service (Union[Unset, bool]):
        importable (Union[Unset, str]):
        keyword (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ProviderOfferingDetailsOEnum]]):
        organization_group_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        scope_uuid (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):
        state (Union[Unset, list[OfferingState]]):
        tag (Union[Unset, list[UUID]]):
        tag_name (Union[Unset, list[str]]):
        tag_names_and (Union[Unset, str]):
        tags_and (Union[Unset, str]):
        type_ (Union[Unset, list[str]]):
        user_has_consent (Union[Unset, bool]):
        user_has_offering_user (Union[Unset, bool]):
        uuid_list (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            accessible_via_calls=accessible_via_calls,
            allowed_customer_uuid=allowed_customer_uuid,
            attributes=attributes,
            billable=billable,
            can_create_offering_user=can_create_offering_user,
            category_group_uuid=category_group_uuid,
            category_uuid=category_uuid,
            created=created,
            customer=customer,
            customer_uuid=customer_uuid,
            description=description,
            has_active_terms_of_service=has_active_terms_of_service,
            has_terms_of_service=has_terms_of_service,
            importable=importable,
            keyword=keyword,
            modified=modified,
            name=name,
            name_exact=name_exact,
            o=o,
            organization_group_uuid=organization_group_uuid,
            page=page,
            page_size=page_size,
            parent_uuid=parent_uuid,
            project_uuid=project_uuid,
            query=query,
            resource_customer_uuid=resource_customer_uuid,
            resource_project_uuid=resource_project_uuid,
            scope_uuid=scope_uuid,
            service_manager_uuid=service_manager_uuid,
            shared=shared,
            state=state,
            tag=tag,
            tag_name=tag_name,
            tag_names_and=tag_names_and,
            tags_and=tags_and,
            type_=type_,
            user_has_consent=user_has_consent,
            user_has_offering_user=user_has_offering_user,
            uuid_list=uuid_list,
        )
    ).parsed
