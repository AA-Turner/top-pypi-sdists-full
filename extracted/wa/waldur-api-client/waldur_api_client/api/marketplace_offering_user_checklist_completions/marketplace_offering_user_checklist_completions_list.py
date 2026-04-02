import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_checklist_completion import UserChecklistCompletion
from ...models.user_checklist_completion_o_enum import UserChecklistCompletionOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    params["is_completed"] = is_completed

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-offering-user-checklist-completions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["UserChecklistCompletion"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserChecklistCompletion.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["UserChecklistCompletion"]]:
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
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["UserChecklistCompletion"]]:
    """List checklist completions for offering users


            Returns a paginated list of all checklist completions for offering users that the current
    user is allowed to see.
            This endpoint is used by service providers to monitor compliance status and by users to see
    their own required checklists.
            Visibility follows the same rules as the `OfferingUsers` endpoint.


    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserChecklistCompletion']]
    """

    kwargs = _get_kwargs(
        created=created,
        is_completed=is_completed,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserChecklistCompletion"]:
    """List checklist completions for offering users


            Returns a paginated list of all checklist completions for offering users that the current
    user is allowed to see.
            This endpoint is used by service providers to monitor compliance status and by users to see
    their own required checklists.
            Visibility follows the same rules as the `OfferingUsers` endpoint.


    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserChecklistCompletion']
    """

    return sync_detailed(
        client=client,
        created=created,
        is_completed=is_completed,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["UserChecklistCompletion"]]:
    """List checklist completions for offering users


            Returns a paginated list of all checklist completions for offering users that the current
    user is allowed to see.
            This endpoint is used by service providers to monitor compliance status and by users to see
    their own required checklists.
            Visibility follows the same rules as the `OfferingUsers` endpoint.


    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserChecklistCompletion']]
    """

    kwargs = _get_kwargs(
        created=created,
        is_completed=is_completed,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserChecklistCompletion"]:
    """List checklist completions for offering users


            Returns a paginated list of all checklist completions for offering users that the current
    user is allowed to see.
            This endpoint is used by service providers to monitor compliance status and by users to see
    their own required checklists.
            Visibility follows the same rules as the `OfferingUsers` endpoint.


    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserChecklistCompletion']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            is_completed=is_completed,
            modified=modified,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserChecklistCompletion"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserChecklistCompletion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserChecklistCompletion] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        is_completed=is_completed,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
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
    created: Union[Unset, datetime.datetime] = UNSET,
    is_completed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[UserChecklistCompletionOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserChecklistCompletion"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        is_completed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[UserChecklistCompletionOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserChecklistCompletion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserChecklistCompletion] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        is_completed=is_completed,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
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
