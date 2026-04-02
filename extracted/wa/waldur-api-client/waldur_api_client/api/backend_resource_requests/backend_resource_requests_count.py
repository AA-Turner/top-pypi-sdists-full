import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_req_o_enum import BackendResourceReqOEnum
from ...models.backend_resource_req_state_enum import BackendResourceReqStateEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    finished: Union[Unset, datetime.datetime] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    started: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[BackendResourceReqStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_finished: Union[Unset, str] = UNSET
    if not isinstance(finished, Unset):
        json_finished = finished.isoformat()
    params["finished"] = json_finished

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

    json_started: Union[Unset, str] = UNSET
    if not isinstance(started, Unset):
        json_started = started.isoformat()
    params["started"] = json_started

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/backend-resource-requests/",
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
    finished: Union[Unset, datetime.datetime] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    started: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[BackendResourceReqStateEnum]] = UNSET,
) -> Response[int]:
    """List backend resource requests

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        finished (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        started (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[BackendResourceReqStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created=created,
        finished=finished,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        started=started,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    finished: Union[Unset, datetime.datetime] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    started: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[BackendResourceReqStateEnum]] = UNSET,
) -> int:
    """List backend resource requests

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        finished (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        started (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[BackendResourceReqStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        created=created,
        finished=finished,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        started=started,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    finished: Union[Unset, datetime.datetime] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    started: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[BackendResourceReqStateEnum]] = UNSET,
) -> Response[int]:
    """List backend resource requests

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        finished (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        started (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[BackendResourceReqStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created=created,
        finished=finished,
        modified=modified,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        started=started,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    finished: Union[Unset, datetime.datetime] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    started: Union[Unset, datetime.datetime] = UNSET,
    state: Union[Unset, list[BackendResourceReqStateEnum]] = UNSET,
) -> int:
    """List backend resource requests

     Get number of items in the collection matching the request parameters.

    Args:
        created (Union[Unset, datetime.datetime]):
        finished (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        started (Union[Unset, datetime.datetime]):
        state (Union[Unset, list[BackendResourceReqStateEnum]]):

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
            finished=finished,
            modified=modified,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            started=started,
            state=state,
        )
    ).parsed
