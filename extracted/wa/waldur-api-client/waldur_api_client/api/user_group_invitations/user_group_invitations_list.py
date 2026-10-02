from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_req_o_enum import BackendResourceReqOEnum
from ...models.group_invitation import GroupInvitation
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["is_active"] = is_active

    params["is_public"] = is_public

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

    params["scope"] = scope

    params["scope_type"] = scope_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/user-group-invitations/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["GroupInvitation"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GroupInvitation.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["GroupInvitation"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> Response[list["GroupInvitation"]]:
    """List group invitations

     Retrieve a list of group invitations. Unauthenticated users can only see public invitations.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GroupInvitation']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> list["GroupInvitation"]:
    """List group invitations

     Retrieve a list of group invitations. Unauthenticated users can only see public invitations.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupInvitation']
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> Response[list["GroupInvitation"]]:
    """List group invitations

     Retrieve a list of group invitations. Unauthenticated users can only see public invitations.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GroupInvitation']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> list["GroupInvitation"]:
    """List group invitations

     Retrieve a list of group invitations. Unauthenticated users can only see public invitations.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupInvitation']
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            is_active=is_active,
            is_public=is_public,
            o=o,
            page=page,
            page_size=page_size,
            role_name=role_name,
            role_uuid=role_uuid,
            scope=scope,
            scope_type=scope_type,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> list["GroupInvitation"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupInvitation']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[GroupInvitation] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
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
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> list["GroupInvitation"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GroupInvitation']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[GroupInvitation] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
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
