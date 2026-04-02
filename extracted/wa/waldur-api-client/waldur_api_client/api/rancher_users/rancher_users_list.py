from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rancher_user import RancherUser
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_cluster_uuid: Union[Unset, str] = UNSET
    if not isinstance(cluster_uuid, Unset):
        json_cluster_uuid = str(cluster_uuid)
    params["cluster_uuid"] = json_cluster_uuid

    params["is_active"] = is_active

    params["page"] = page

    params["page_size"] = page_size

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["user_full_name"] = user_full_name

    params["user_username"] = user_username

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/rancher-users/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["RancherUser"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RancherUser.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["RancherUser"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["RancherUser"]]:
    """
    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RancherUser']]
    """

    kwargs = _get_kwargs(
        cluster_uuid=cluster_uuid,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings_uuid=settings_uuid,
        user_full_name=user_full_name,
        user_username=user_username,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherUser"]:
    """
    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherUser']
    """

    return sync_detailed(
        client=client,
        cluster_uuid=cluster_uuid,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings_uuid=settings_uuid,
        user_full_name=user_full_name,
        user_username=user_username,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["RancherUser"]]:
    """
    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RancherUser']]
    """

    kwargs = _get_kwargs(
        cluster_uuid=cluster_uuid,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings_uuid=settings_uuid,
        user_full_name=user_full_name,
        user_username=user_username,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherUser"]:
    """
    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherUser']
    """

    return (
        await asyncio_detailed(
            client=client,
            cluster_uuid=cluster_uuid,
            is_active=is_active,
            page=page,
            page_size=page_size,
            settings_uuid=settings_uuid,
            user_full_name=user_full_name,
            user_username=user_username,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherUser"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RancherUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        cluster_uuid=cluster_uuid,
        is_active=is_active,
        settings_uuid=settings_uuid,
        user_full_name=user_full_name,
        user_username=user_username,
        user_uuid=user_uuid,
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
    cluster_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["RancherUser"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        cluster_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        settings_uuid (Union[Unset, UUID]):
        user_full_name (Union[Unset, str]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RancherUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RancherUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        cluster_uuid=cluster_uuid,
        is_active=is_active,
        settings_uuid=settings_uuid,
        user_full_name=user_full_name,
        user_username=user_username,
        user_uuid=user_uuid,
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
