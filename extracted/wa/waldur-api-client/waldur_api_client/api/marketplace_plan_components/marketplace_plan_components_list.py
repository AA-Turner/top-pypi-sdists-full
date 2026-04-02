from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plan_component import PlanComponent
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["archived"] = archived

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_plan_uuid: Union[Unset, str] = UNSET
    if not isinstance(plan_uuid, Unset):
        json_plan_uuid = str(plan_uuid)
    params["plan_uuid"] = json_plan_uuid

    params["shared"] = shared

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-plan-components/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["PlanComponent"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PlanComponent.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PlanComponent"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> Response[list["PlanComponent"]]:
    """List plan components

     Returns a paginated list of all plan components. A plan component defines the pricing and quotas for
    an offering component within a billing plan. The list is filtered based on the current user's access
    permissions and organization group memberships.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PlanComponent']]
    """

    kwargs = _get_kwargs(
        archived=archived,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        plan_uuid=plan_uuid,
        shared=shared,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> list["PlanComponent"]:
    """List plan components

     Returns a paginated list of all plan components. A plan component defines the pricing and quotas for
    an offering component within a billing plan. The list is filtered based on the current user's access
    permissions and organization group memberships.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlanComponent']
    """

    return sync_detailed(
        client=client,
        archived=archived,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        plan_uuid=plan_uuid,
        shared=shared,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> Response[list["PlanComponent"]]:
    """List plan components

     Returns a paginated list of all plan components. A plan component defines the pricing and quotas for
    an offering component within a billing plan. The list is filtered based on the current user's access
    permissions and organization group memberships.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PlanComponent']]
    """

    kwargs = _get_kwargs(
        archived=archived,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        plan_uuid=plan_uuid,
        shared=shared,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> list["PlanComponent"]:
    """List plan components

     Returns a paginated list of all plan components. A plan component defines the pricing and quotas for
    an offering component within a billing plan. The list is filtered based on the current user's access
    permissions and organization group memberships.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlanComponent']
    """

    return (
        await asyncio_detailed(
            client=client,
            archived=archived,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            plan_uuid=plan_uuid,
            shared=shared,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> list["PlanComponent"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlanComponent']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PlanComponent] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        archived=archived,
        offering_uuid=offering_uuid,
        plan_uuid=plan_uuid,
        shared=shared,
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
    archived: Union[Unset, bool] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    shared: Union[Unset, bool] = UNSET,
) -> list["PlanComponent"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        archived (Union[Unset, bool]):
        offering_uuid (Union[Unset, UUID]):
        plan_uuid (Union[Unset, UUID]):
        shared (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PlanComponent']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PlanComponent] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        archived=archived,
        offering_uuid=offering_uuid,
        plan_uuid=plan_uuid,
        shared=shared,
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
