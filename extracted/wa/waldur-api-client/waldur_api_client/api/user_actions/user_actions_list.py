import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.urgency_enum import UrgencyEnum
from ...models.user_action import UserAction
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["action_type"] = action_type

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    params["due_within_days"] = due_within_days

    params["include_silenced"] = include_silenced

    params["is_silenced"] = is_silenced

    params["o"] = o

    params["overdue"] = overdue

    params["page"] = page

    params["page_size"] = page_size

    json_urgency: Union[Unset, str] = UNSET
    if not isinstance(urgency, Unset):
        json_urgency = urgency.value

    params["urgency"] = json_urgency

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/user-actions/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["UserAction"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserAction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["UserAction"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["UserAction"]]:
    """
    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserAction']]
    """

    kwargs = _get_kwargs(
        action_type=action_type,
        created_after=created_after,
        created_before=created_before,
        due_within_days=due_within_days,
        include_silenced=include_silenced,
        is_silenced=is_silenced,
        o=o,
        overdue=overdue,
        page=page,
        page_size=page_size,
        urgency=urgency,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserAction"]:
    """
    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAction']
    """

    return sync_detailed(
        client=client,
        action_type=action_type,
        created_after=created_after,
        created_before=created_before,
        due_within_days=due_within_days,
        include_silenced=include_silenced,
        is_silenced=is_silenced,
        o=o,
        overdue=overdue,
        page=page,
        page_size=page_size,
        urgency=urgency,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["UserAction"]]:
    """
    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserAction']]
    """

    kwargs = _get_kwargs(
        action_type=action_type,
        created_after=created_after,
        created_before=created_before,
        due_within_days=due_within_days,
        include_silenced=include_silenced,
        is_silenced=is_silenced,
        o=o,
        overdue=overdue,
        page=page,
        page_size=page_size,
        urgency=urgency,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserAction"]:
    """
    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAction']
    """

    return (
        await asyncio_detailed(
            client=client,
            action_type=action_type,
            created_after=created_after,
            created_before=created_before,
            due_within_days=due_within_days,
            include_silenced=include_silenced,
            is_silenced=is_silenced,
            o=o,
            overdue=overdue,
            page=page,
            page_size=page_size,
            urgency=urgency,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserAction"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAction']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserAction] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        action_type=action_type,
        created_after=created_after,
        created_before=created_before,
        due_within_days=due_within_days,
        include_silenced=include_silenced,
        is_silenced=is_silenced,
        o=o,
        overdue=overdue,
        urgency=urgency,
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
    action_type: Union[Unset, str] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    due_within_days: Union[Unset, float] = UNSET,
    include_silenced: Union[Unset, bool] = UNSET,
    is_silenced: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    overdue: Union[Unset, bool] = UNSET,
    urgency: Union[Unset, UrgencyEnum] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["UserAction"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        action_type (Union[Unset, str]):
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        due_within_days (Union[Unset, float]):
        include_silenced (Union[Unset, bool]):
        is_silenced (Union[Unset, bool]):
        o (Union[Unset, str]):
        overdue (Union[Unset, bool]):
        urgency (Union[Unset, UrgencyEnum]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAction']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserAction] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        action_type=action_type,
        created_after=created_after,
        created_before=created_before,
        due_within_days=due_within_days,
        include_silenced=include_silenced,
        is_silenced=is_silenced,
        o=o,
        overdue=overdue,
        urgency=urgency,
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
