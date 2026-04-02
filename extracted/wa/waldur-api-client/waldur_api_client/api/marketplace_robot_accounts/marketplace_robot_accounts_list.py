import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_resource_sync_status_remote_state_enum import RemoteResourceSyncStatusRemoteStateEnum
from ...models.robot_account_details import RobotAccountDetails
from ...models.robot_account_details_field_enum import RobotAccountDetailsFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["page"] = page

    params["page_size"] = page_size

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["resource"] = resource

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_state: Union[Unset, int] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-robot-accounts/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["RobotAccountDetails"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RobotAccountDetails.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["RobotAccountDetails"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Response[list["RobotAccountDetails"]]:
    """List robot accounts

     Returns a paginated list of robot accounts accessible to the current user.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RobotAccountDetails']]
    """

    kwargs = _get_kwargs(
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        state=state,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> list["RobotAccountDetails"]:
    """List robot accounts

     Returns a paginated list of robot accounts accessible to the current user.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RobotAccountDetails']
    """

    return sync_detailed(
        client=client,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        state=state,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Response[list["RobotAccountDetails"]]:
    """List robot accounts

     Returns a paginated list of robot accounts accessible to the current user.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RobotAccountDetails']]
    """

    kwargs = _get_kwargs(
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        state=state,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> list["RobotAccountDetails"]:
    """List robot accounts

     Returns a paginated list of robot accounts accessible to the current user.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RobotAccountDetails']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            customer_uuid=customer_uuid,
            field=field,
            modified=modified,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            provider_uuid=provider_uuid,
            resource=resource,
            resource_uuid=resource_uuid,
            state=state,
            type_=type_,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> list["RobotAccountDetails"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RobotAccountDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RobotAccountDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        state=state,
        type_=type_,
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
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[RobotAccountDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, RemoteResourceSyncStatusRemoteStateEnum] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> list["RobotAccountDetails"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[RobotAccountDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, RemoteResourceSyncStatusRemoteStateEnum]):
        type_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RobotAccountDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RobotAccountDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        state=state,
        type_=type_,
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
