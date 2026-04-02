from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.version_history import VersionHistory
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["offering"] = offering

    json_offering_slug: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_slug, Unset):
        json_offering_slug = offering_slug

    params["offering_slug"] = json_offering_slug

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_parent_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_offering_uuid, Unset):
        json_parent_offering_uuid = str(parent_offering_uuid)
    params["parent_offering_uuid"] = json_parent_offering_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-plans/{uuid}/history/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["VersionHistory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VersionHistory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["VersionHistory"]]:
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
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        created_after=created_after,
        created_before=created_before,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        created_after=created_after,
        created_before=created_before,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        created_after=created_after,
        created_before=created_before,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            created_after=created_after,
            created_before=created_before,
            offering=offering,
            offering_slug=offering_slug,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            parent_offering_uuid=parent_offering_uuid,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        created_after=created_after,
        created_before=created_before,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
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
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        parent_offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        created_after=created_after,
        created_before=created_before,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
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
