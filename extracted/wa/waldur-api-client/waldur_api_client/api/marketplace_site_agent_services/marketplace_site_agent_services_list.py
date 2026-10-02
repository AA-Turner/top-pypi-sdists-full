import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_service import AgentService
from ...models.agent_service_state_enum import AgentServiceStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_identity_uuid: Union[Unset, str] = UNSET
    if not isinstance(identity_uuid, Unset):
        json_identity_uuid = str(identity_uuid)
    params["identity_uuid"] = json_identity_uuid

    params["mode"] = mode

    json_modified_after: Union[Unset, str] = UNSET
    if not isinstance(modified_after, Unset):
        json_modified_after = modified_after.isoformat()
    params["modified_after"] = json_modified_after

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

    params["page"] = page

    params["page_size"] = page_size

    params["stale"] = stale

    json_state: Union[Unset, list[int]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-site-agent-services/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["AgentService"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AgentService.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AgentService"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> Response[list["AgentService"]]:
    """
    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AgentService']]
    """

    kwargs = _get_kwargs(
        identity_uuid=identity_uuid,
        mode=mode,
        modified_after=modified_after,
        modified_before=modified_before,
        page=page,
        page_size=page_size,
        stale=stale,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> list["AgentService"]:
    """
    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentService']
    """

    return sync_detailed(
        client=client,
        identity_uuid=identity_uuid,
        mode=mode,
        modified_after=modified_after,
        modified_before=modified_before,
        page=page,
        page_size=page_size,
        stale=stale,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> Response[list["AgentService"]]:
    """
    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AgentService']]
    """

    kwargs = _get_kwargs(
        identity_uuid=identity_uuid,
        mode=mode,
        modified_after=modified_after,
        modified_before=modified_before,
        page=page,
        page_size=page_size,
        stale=stale,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> list["AgentService"]:
    """
    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentService']
    """

    return (
        await asyncio_detailed(
            client=client,
            identity_uuid=identity_uuid,
            mode=mode,
            modified_after=modified_after,
            modified_before=modified_before,
            page=page,
            page_size=page_size,
            stale=stale,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> list["AgentService"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentService']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AgentService] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        identity_uuid=identity_uuid,
        mode=mode,
        modified_after=modified_after,
        modified_before=modified_before,
        stale=stale,
        state=state,
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
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> list["AgentService"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        identity_uuid (Union[Unset, UUID]):
        mode (Union[Unset, str]):
        modified_after (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        stale (Union[Unset, bool]):
        state (Union[Unset, list[AgentServiceStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentService']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AgentService] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        identity_uuid=identity_uuid,
        mode=mode,
        modified_after=modified_after,
        modified_before=modified_before,
        stale=stale,
        state=state,
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
