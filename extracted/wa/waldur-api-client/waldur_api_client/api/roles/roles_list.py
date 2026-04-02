from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.role_details import RoleDetails
from ...models.role_details_field_enum import RoleDetailsFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["description"] = description

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["is_active"] = is_active

    params["name"] = name

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/roles/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["RoleDetails"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RoleDetails.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["RoleDetails"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["RoleDetails"]]:
    """List roles

     Get a list of all available roles.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RoleDetails']]
    """

    kwargs = _get_kwargs(
        description=description,
        field=field,
        is_active=is_active,
        name=name,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["RoleDetails"]:
    """List roles

     Get a list of all available roles.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RoleDetails']
    """

    return sync_detailed(
        client=client,
        description=description,
        field=field,
        is_active=is_active,
        name=name,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["RoleDetails"]]:
    """List roles

     Get a list of all available roles.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RoleDetails']]
    """

    kwargs = _get_kwargs(
        description=description,
        field=field,
        is_active=is_active,
        name=name,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["RoleDetails"]:
    """List roles

     Get a list of all available roles.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RoleDetails']
    """

    return (
        await asyncio_detailed(
            client=client,
            description=description,
            field=field,
            is_active=is_active,
            name=name,
            page=page,
            page_size=page_size,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> list["RoleDetails"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RoleDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RoleDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        description=description,
        field=field,
        is_active=is_active,
        name=name,
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
    description: Union[Unset, str] = UNSET,
    field: Union[Unset, list[RoleDetailsFieldEnum]] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
) -> list["RoleDetails"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        description (Union[Unset, str]):
        field (Union[Unset, list[RoleDetailsFieldEnum]]):
        is_active (Union[Unset, bool]):
        name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RoleDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RoleDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        description=description,
        field=field,
        is_active=is_active,
        name=name,
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
