import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_service_state_enum import AgentServiceStateEnum
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/marketplace-site-agent-services/",
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
    identity_uuid: Union[Unset, UUID] = UNSET,
    mode: Union[Unset, str] = UNSET,
    modified_after: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    stale: Union[Unset, bool] = UNSET,
    state: Union[Unset, list[AgentServiceStateEnum]] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
