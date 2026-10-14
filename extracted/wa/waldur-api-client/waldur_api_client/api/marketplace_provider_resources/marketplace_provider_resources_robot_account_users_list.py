from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.basic_user import BasicUser
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    full_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["full_name"] = full_name

    params["page"] = page

    params["page_size"] = page_size

    params["user_keyword"] = user_keyword

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-provider-resources/{uuid}/robot_account_users/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["BasicUser"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BasicUser.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["BasicUser"]]:
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
    full_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> Response[list["BasicUser"]]:
    """List users a robot account on this resource may link

     Returns the project and organization users of this resource that a robot account may link as users
    or as the responsible user. When ENFORCE_USER_CONSENT_FOR_OFFERINGS is enabled and the offering has
    active Terms of Service, only users with active consent are returned, for every caller.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BasicUser']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        full_name=full_name,
        page=page,
        page_size=page_size,
        user_keyword=user_keyword,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    full_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> list["BasicUser"]:
    """List users a robot account on this resource may link

     Returns the project and organization users of this resource that a robot account may link as users
    or as the responsible user. When ENFORCE_USER_CONSENT_FOR_OFFERINGS is enabled and the offering has
    active Terms of Service, only users with active consent are returned, for every caller.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BasicUser']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        full_name=full_name,
        page=page,
        page_size=page_size,
        user_keyword=user_keyword,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    full_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> Response[list["BasicUser"]]:
    """List users a robot account on this resource may link

     Returns the project and organization users of this resource that a robot account may link as users
    or as the responsible user. When ENFORCE_USER_CONSENT_FOR_OFFERINGS is enabled and the offering has
    active Terms of Service, only users with active consent are returned, for every caller.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BasicUser']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        full_name=full_name,
        page=page,
        page_size=page_size,
        user_keyword=user_keyword,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    full_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> list["BasicUser"]:
    """List users a robot account on this resource may link

     Returns the project and organization users of this resource that a robot account may link as users
    or as the responsible user. When ENFORCE_USER_CONSENT_FOR_OFFERINGS is enabled and the offering has
    active Terms of Service, only users with active consent are returned, for every caller.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BasicUser']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            full_name=full_name,
            page=page,
            page_size=page_size,
            user_keyword=user_keyword,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    full_name: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> list["BasicUser"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BasicUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[BasicUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        full_name=full_name,
        user_keyword=user_keyword,
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
    full_name: Union[Unset, str] = UNSET,
    user_keyword: Union[Unset, str] = UNSET,
) -> list["BasicUser"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        full_name (Union[Unset, str]):
        user_keyword (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BasicUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[BasicUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        full_name=full_name,
        user_keyword=user_keyword,
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
