import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_action import ResourceApiKeyAction
from ...models.resource_api_key_state import ResourceApiKeyState
from ...models.resource_api_key_status import ResourceApiKeyStatus
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["has_pending_action"] = has_pending_action

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_pending_action: Union[Unset, list[str]] = UNSET
    if not isinstance(pending_action, Unset):
        json_pending_action = []
        for pending_action_item_data in pending_action:
            pending_action_item = pending_action_item_data.value
            json_pending_action.append(pending_action_item)

    params["pending_action"] = json_pending_action

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-resource-api-keys/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ResourceApiKeyStatus"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ResourceApiKeyStatus.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ResourceApiKeyStatus"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ResourceApiKeyStatus"]]:
    """
    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ResourceApiKeyStatus']]
    """

    kwargs = _get_kwargs(
        has_pending_action=has_pending_action,
        modified_before=modified_before,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pending_action=pending_action,
        resource_uuid=resource_uuid,
        state=state,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["ResourceApiKeyStatus"]:
    """
    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ResourceApiKeyStatus']
    """

    return sync_detailed(
        client=client,
        has_pending_action=has_pending_action,
        modified_before=modified_before,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pending_action=pending_action,
        resource_uuid=resource_uuid,
        state=state,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ResourceApiKeyStatus"]]:
    """
    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ResourceApiKeyStatus']]
    """

    kwargs = _get_kwargs(
        has_pending_action=has_pending_action,
        modified_before=modified_before,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pending_action=pending_action,
        resource_uuid=resource_uuid,
        state=state,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["ResourceApiKeyStatus"]:
    """
    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ResourceApiKeyStatus']
    """

    return (
        await asyncio_detailed(
            client=client,
            has_pending_action=has_pending_action,
            modified_before=modified_before,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            pending_action=pending_action,
            resource_uuid=resource_uuid,
            state=state,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["ResourceApiKeyStatus"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ResourceApiKeyStatus']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ResourceApiKeyStatus] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        has_pending_action=has_pending_action,
        modified_before=modified_before,
        offering_uuid=offering_uuid,
        pending_action=pending_action,
        resource_uuid=resource_uuid,
        state=state,
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
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["ResourceApiKeyStatus"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        has_pending_action (Union[Unset, bool]):
        modified_before (Union[Unset, datetime.datetime]):
        offering_uuid (Union[Unset, UUID]):
        pending_action (Union[Unset, list[ResourceApiKeyAction]]):
        resource_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceApiKeyState]]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ResourceApiKeyStatus']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ResourceApiKeyStatus] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        has_pending_action=has_pending_action,
        modified_before=modified_before,
        offering_uuid=offering_uuid,
        pending_action=pending_action,
        resource_uuid=resource_uuid,
        state=state,
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
