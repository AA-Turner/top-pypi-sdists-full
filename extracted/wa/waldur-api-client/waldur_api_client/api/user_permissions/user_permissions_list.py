import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_permission_o_enum import OfferingPermissionOEnum
from ...models.permission import Permission
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_expiration_time: Union[Unset, str] = UNSET
    if not isinstance(expiration_time, Unset):
        json_expiration_time = expiration_time.isoformat()
    params["expiration_time"] = json_expiration_time

    params["full_name"] = full_name

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

    params["page"] = page

    params["page_size"] = page_size

    params["role_name"] = role_name

    json_role_uuid: Union[Unset, str] = UNSET
    if not isinstance(role_uuid, Unset):
        json_role_uuid = str(role_uuid)
    params["role_uuid"] = json_role_uuid

    params["scope_name"] = scope_name

    params["scope_type"] = scope_type

    params["scope_uuid"] = scope_uuid

    json_user: Union[Unset, str] = UNSET
    if not isinstance(user, Unset):
        json_user = str(user)
    params["user"] = json_user

    params["user_slug"] = user_slug

    params["user_url"] = user_url

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/user-permissions/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Permission"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Permission.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Permission"]]:
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
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["Permission"]]:
    """List user permissions

     Get a list of all permissions for the current user. Staff and support users can view all user
    permissions. The list can be filtered by user, scope, role, etc.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Permission']]
    """

    kwargs = _get_kwargs(
        created=created,
        expiration_time=expiration_time,
        full_name=full_name,
        modified=modified,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope_name=scope_name,
        scope_type=scope_type,
        scope_uuid=scope_uuid,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["Permission"]:
    """List user permissions

     Get a list of all permissions for the current user. Staff and support users can view all user
    permissions. The list can be filtered by user, scope, role, etc.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Permission']
    """

    return sync_detailed(
        client=client,
        created=created,
        expiration_time=expiration_time,
        full_name=full_name,
        modified=modified,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope_name=scope_name,
        scope_type=scope_type,
        scope_uuid=scope_uuid,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["Permission"]]:
    """List user permissions

     Get a list of all permissions for the current user. Staff and support users can view all user
    permissions. The list can be filtered by user, scope, role, etc.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Permission']]
    """

    kwargs = _get_kwargs(
        created=created,
        expiration_time=expiration_time,
        full_name=full_name,
        modified=modified,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope_name=scope_name,
        scope_type=scope_type,
        scope_uuid=scope_uuid,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["Permission"]:
    """List user permissions

     Get a list of all permissions for the current user. Staff and support users can view all user
    permissions. The list can be filtered by user, scope, role, etc.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Permission']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            expiration_time=expiration_time,
            full_name=full_name,
            modified=modified,
            native_name=native_name,
            o=o,
            page=page,
            page_size=page_size,
            role_name=role_name,
            role_uuid=role_uuid,
            scope_name=scope_name,
            scope_type=scope_type,
            scope_uuid=scope_uuid,
            user=user,
            user_slug=user_slug,
            user_url=user_url,
            username=username,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["Permission"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Permission']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Permission] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        expiration_time=expiration_time,
        full_name=full_name,
        modified=modified,
        native_name=native_name,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope_name=scope_name,
        scope_type=scope_type,
        scope_uuid=scope_uuid,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
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
    expiration_time: Union[Unset, datetime.datetime] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OfferingPermissionOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    scope_uuid: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["Permission"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        expiration_time (Union[Unset, datetime.datetime]):
        full_name (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[OfferingPermissionOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        scope_uuid (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Permission']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Permission] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        expiration_time=expiration_time,
        full_name=full_name,
        modified=modified,
        native_name=native_name,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope_name=scope_name,
        scope_type=scope_type,
        scope_uuid=scope_uuid,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
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
