from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_role_details import UserRoleDetails
from ...models.user_role_details_field_enum import UserRoleDetailsFieldEnum
from ...models.user_role_details_o_enum import UserRoleDetailsOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["full_name"] = full_name

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

    json_role: Union[Unset, str] = UNSET
    if not isinstance(role, Unset):
        json_role = str(role)
    params["role"] = json_role

    params["search_string"] = search_string

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
        "url": f"/api/proposal-proposals/{uuid}/list_users/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["UserRoleDetails"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserRoleDetails.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["UserRoleDetails"]]:
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
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["UserRoleDetails"]]:
    """List users and their roles in a scope

     Retrieves a list of users who have a role within a specific scope (e.g., a project or an
    organization). The list can be filtered by user details or role.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserRoleDetails']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["UserRoleDetails"]:
    """List users and their roles in a scope

     Retrieves a list of users who have a role within a specific scope (e.g., a project or an
    organization). The list can be filtered by user details or role.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserRoleDetails']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["UserRoleDetails"]]:
    """List users and their roles in a scope

     Retrieves a list of users who have a role within a specific scope (e.g., a project or an
    organization). The list can be filtered by user details or role.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserRoleDetails']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["UserRoleDetails"]:
    """List users and their roles in a scope

     Retrieves a list of users who have a role within a specific scope (e.g., a project or an
    organization). The list can be filtered by user details or role.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserRoleDetails']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            field=field,
            full_name=full_name,
            native_name=native_name,
            o=o,
            page=page,
            page_size=page_size,
            role=role,
            search_string=search_string,
            user=user,
            user_slug=user_slug,
            user_url=user_url,
            username=username,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["UserRoleDetails"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserRoleDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserRoleDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        role=role,
        search_string=search_string,
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    role: Union[Unset, UUID] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["UserRoleDetails"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        role (Union[Unset, UUID]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserRoleDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserRoleDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        role=role,
        search_string=search_string,
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
