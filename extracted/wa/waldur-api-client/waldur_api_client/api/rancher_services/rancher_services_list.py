from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.core_states import CoreStates
from ...models.rancher_service import RancherService
from ...models.rancher_service_field_enum import RancherServiceFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["backend_id"] = backend_id

    params["can_manage"] = can_manage

    json_cluster_uuid: Union[Unset, str] = UNSET
    if not isinstance(cluster_uuid, Unset):
        json_cluster_uuid = str(cluster_uuid)
    params["cluster_uuid"] = json_cluster_uuid

    json_customer: Union[Unset, str] = UNSET
    if not isinstance(customer, Unset):
        json_customer = str(customer)
    params["customer"] = json_customer

    params["customer_abbreviation"] = customer_abbreviation

    params["customer_name"] = customer_name

    params["customer_native_name"] = customer_native_name

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["description"] = description

    params["external_ip"] = external_ip

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["name"] = name

    params["name_exact"] = name_exact

    json_namespace_uuid: Union[Unset, str] = UNSET
    if not isinstance(namespace_uuid, Unset):
        json_namespace_uuid = str(namespace_uuid)
    params["namespace_uuid"] = json_namespace_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_project: Union[Unset, str] = UNSET
    if not isinstance(project, Unset):
        json_project = str(project)
    params["project"] = json_project

    params["project_name"] = project_name

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_rancher_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(rancher_project_uuid, Unset):
        json_rancher_project_uuid = str(rancher_project_uuid)
    params["rancher_project_uuid"] = json_rancher_project_uuid

    params["service_settings_name"] = service_settings_name

    json_service_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_settings_uuid, Unset):
        json_service_settings_uuid = str(service_settings_uuid)
    params["service_settings_uuid"] = json_service_settings_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_uuid: Union[Unset, str] = UNSET
    if not isinstance(uuid, Unset):
        json_uuid = str(uuid)
    params["uuid"] = json_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/rancher-services/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["RancherService"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RancherService.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["RancherService"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["RancherService"]]:
    """
    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RancherService']]
    """

    kwargs = _get_kwargs(
        backend_id=backend_id,
        can_manage=can_manage,
        cluster_uuid=cluster_uuid,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        name=name,
        name_exact=name_exact,
        namespace_uuid=namespace_uuid,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        rancher_project_uuid=rancher_project_uuid,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        state=state,
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherService"]:
    """
    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherService']
    """

    return sync_detailed(
        client=client,
        backend_id=backend_id,
        can_manage=can_manage,
        cluster_uuid=cluster_uuid,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        name=name,
        name_exact=name_exact,
        namespace_uuid=namespace_uuid,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        rancher_project_uuid=rancher_project_uuid,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        state=state,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["RancherService"]]:
    """
    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RancherService']]
    """

    kwargs = _get_kwargs(
        backend_id=backend_id,
        can_manage=can_manage,
        cluster_uuid=cluster_uuid,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        name=name,
        name_exact=name_exact,
        namespace_uuid=namespace_uuid,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        rancher_project_uuid=rancher_project_uuid,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        state=state,
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherService"]:
    """
    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherService']
    """

    return (
        await asyncio_detailed(
            client=client,
            backend_id=backend_id,
            can_manage=can_manage,
            cluster_uuid=cluster_uuid,
            customer=customer,
            customer_abbreviation=customer_abbreviation,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            customer_uuid=customer_uuid,
            description=description,
            external_ip=external_ip,
            field=field,
            name=name,
            name_exact=name_exact,
            namespace_uuid=namespace_uuid,
            page=page,
            page_size=page_size,
            project=project,
            project_name=project_name,
            project_uuid=project_uuid,
            rancher_project_uuid=rancher_project_uuid,
            service_settings_name=service_settings_name,
            service_settings_uuid=service_settings_uuid,
            state=state,
            uuid=uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherService"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherService']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RancherService] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        backend_id=backend_id,
        can_manage=can_manage,
        cluster_uuid=cluster_uuid,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        name=name,
        name_exact=name_exact,
        namespace_uuid=namespace_uuid,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        rancher_project_uuid=rancher_project_uuid,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        state=state,
        uuid=uuid,
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
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RancherServiceFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    namespace_uuid: Union[Unset, UUID] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    rancher_project_uuid: Union[Unset, UUID] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherService"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        cluster_uuid (Union[Unset, UUID]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[RancherServiceFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        namespace_uuid (Union[Unset, UUID]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        rancher_project_uuid (Union[Unset, UUID]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherService']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RancherService] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        backend_id=backend_id,
        can_manage=can_manage,
        cluster_uuid=cluster_uuid,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        name=name,
        name_exact=name_exact,
        namespace_uuid=namespace_uuid,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        rancher_project_uuid=rancher_project_uuid,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        state=state,
        uuid=uuid,
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
