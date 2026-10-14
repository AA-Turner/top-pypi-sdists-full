import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_action import ResourceApiKeyAction
from ...models.resource_api_key_state import ResourceApiKeyState
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/marketplace-resource-api-keys/",
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
    has_pending_action: Union[Unset, bool] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pending_action: Union[Unset, list[ResourceApiKeyAction]] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceApiKeyState]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
