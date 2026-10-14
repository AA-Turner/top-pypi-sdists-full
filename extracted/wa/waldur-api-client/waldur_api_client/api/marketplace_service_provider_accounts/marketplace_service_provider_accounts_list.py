import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_user_o_enum import OfferingUserOEnum
from ...models.offering_user_state import OfferingUserState
from ...models.runtime_state_enum import RuntimeStateEnum
from ...models.service_provider_account import ServiceProviderAccount
from ...models.service_provider_account_field_enum import ServiceProviderAccountFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["is_restricted"] = is_restricted

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["query"] = query

    json_runtime_state: Union[Unset, list[str]] = UNSET
    if not isinstance(runtime_state, Unset):
        json_runtime_state = []
        for runtime_state_item_data in runtime_state:
            runtime_state_item = runtime_state_item_data.value
            json_runtime_state.append(runtime_state_item)

    params["runtime_state"] = json_runtime_state

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["user_username"] = user_username

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-service-provider-accounts/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ServiceProviderAccount"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ServiceProviderAccount.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ServiceProviderAccount"]]:
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
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ServiceProviderAccount"]]:
    """List service provider accounts


            Returns a paginated list of the accounts a service provider holds for its users --
            one per user per provider, shared by every offering of that provider.
            Scoped to providers whose organization the caller can see.


    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderAccount']]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        field=field,
        is_restricted=is_restricted,
        modified=modified,
        modified_before=modified_before,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
        query=query,
        runtime_state=runtime_state,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ServiceProviderAccount"]:
    """List service provider accounts


            Returns a paginated list of the accounts a service provider holds for its users --
            one per user per provider, shared by every offering of that provider.
            Scoped to providers whose organization the caller can see.


    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderAccount']
    """

    return sync_detailed(
        client=client,
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        field=field,
        is_restricted=is_restricted,
        modified=modified,
        modified_before=modified_before,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
        query=query,
        runtime_state=runtime_state,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["ServiceProviderAccount"]]:
    """List service provider accounts


            Returns a paginated list of the accounts a service provider holds for its users --
            one per user per provider, shared by every offering of that provider.
            Scoped to providers whose organization the caller can see.


    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderAccount']]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        field=field,
        is_restricted=is_restricted,
        modified=modified,
        modified_before=modified_before,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
        query=query,
        runtime_state=runtime_state,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ServiceProviderAccount"]:
    """List service provider accounts


            Returns a paginated list of the accounts a service provider holds for its users --
            one per user per provider, shared by every offering of that provider.
            Scoped to providers whose organization the caller can see.


    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderAccount']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            created_before=created_before,
            customer_uuid=customer_uuid,
            field=field,
            is_restricted=is_restricted,
            modified=modified,
            modified_before=modified_before,
            o=o,
            page=page,
            page_size=page_size,
            provider_uuid=provider_uuid,
            query=query,
            runtime_state=runtime_state,
            state=state,
            user_username=user_username,
            user_uuid=user_uuid,
            username=username,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ServiceProviderAccount"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderAccount']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ServiceProviderAccount] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        field=field,
        is_restricted=is_restricted,
        modified=modified,
        modified_before=modified_before,
        o=o,
        provider_uuid=provider_uuid,
        query=query,
        runtime_state=runtime_state,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
        username=username,
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
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[ServiceProviderAccountFieldEnum]] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    runtime_state: Union[Unset, list[RuntimeStateEnum]] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["ServiceProviderAccount"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[ServiceProviderAccountFieldEnum]]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        runtime_state (Union[Unset, list[RuntimeStateEnum]]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderAccount']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ServiceProviderAccount] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        field=field,
        is_restricted=is_restricted,
        modified=modified,
        modified_before=modified_before,
        o=o,
        provider_uuid=provider_uuid,
        query=query,
        runtime_state=runtime_state,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
        username=username,
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
