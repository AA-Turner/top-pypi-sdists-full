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
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
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
        "method": "head",
        "url": "/api/marketplace-service-provider-accounts/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
) -> Response[int]:
    """List service provider accounts

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
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
) -> int:
    """List service provider accounts

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        int
    """

    return sync_detailed(
        client=client,
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
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
) -> Response[int]:
    """List service provider accounts

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
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
) -> int:
    """List service provider accounts

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            created_before=created_before,
            customer_uuid=customer_uuid,
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
