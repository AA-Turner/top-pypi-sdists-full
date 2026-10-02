from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_round_create_request_request import BulkRoundCreateRequestRequest
from ...models.call_states import CallStates
from ...models.protected_call_o_enum import ProtectedCallOEnum
from ...models.protected_round import ProtectedRound
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    body: BulkRoundCreateRequestRequest,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    open_for_offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["customer"] = customer

    params["customer_keyword"] = customer_keyword

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["has_active_round"] = has_active_round

    params["name"] = name

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

    json_offerings_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(offerings_provider_uuid, Unset):
        json_offerings_provider_uuid = str(offerings_provider_uuid)
    params["offerings_provider_uuid"] = json_offerings_provider_uuid

    json_open_for_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(open_for_offering_uuid, Unset):
        json_open_for_offering_uuid = str(open_for_offering_uuid)
    params["open_for_offering_uuid"] = json_open_for_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["slug"] = slug

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/rounds-bulk-set/",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["ProtectedRound"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = ProtectedRound.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ProtectedRound"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BulkRoundCreateRequestRequest,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    open_for_offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> Response[list["ProtectedRound"]]:
    """Create multiple rounds on a call at a fixed cadence. Spacing is controlled by ``cadence``
    (monthly/quarterly/biannual/yearly/custom). Each round's ``cutoff_time`` is derived as ``start_time
    + submission_window_days``. Fixed-date allocation is not supported in bulk mode.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        open_for_offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[CallStates]]):
        body (BulkRoundCreateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProtectedRound']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        open_for_offering_uuid=open_for_offering_uuid,
        page=page,
        page_size=page_size,
        slug=slug,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BulkRoundCreateRequestRequest,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    open_for_offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ProtectedRound"]:
    """Create multiple rounds on a call at a fixed cadence. Spacing is controlled by ``cadence``
    (monthly/quarterly/biannual/yearly/custom). Each round's ``cutoff_time`` is derived as ``start_time
    + submission_window_days``. Fixed-date allocation is not supported in bulk mode.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        open_for_offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[CallStates]]):
        body (BulkRoundCreateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProtectedRound']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        open_for_offering_uuid=open_for_offering_uuid,
        page=page,
        page_size=page_size,
        slug=slug,
        state=state,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BulkRoundCreateRequestRequest,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    open_for_offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> Response[list["ProtectedRound"]]:
    """Create multiple rounds on a call at a fixed cadence. Spacing is controlled by ``cadence``
    (monthly/quarterly/biannual/yearly/custom). Each round's ``cutoff_time`` is derived as ``start_time
    + submission_window_days``. Fixed-date allocation is not supported in bulk mode.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        open_for_offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[CallStates]]):
        body (BulkRoundCreateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProtectedRound']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        open_for_offering_uuid=open_for_offering_uuid,
        page=page,
        page_size=page_size,
        slug=slug,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: BulkRoundCreateRequestRequest,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    open_for_offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    slug: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ProtectedRound"]:
    """Create multiple rounds on a call at a fixed cadence. Spacing is controlled by ``cadence``
    (monthly/quarterly/biannual/yearly/custom). Each round's ``cutoff_time`` is derived as ``start_time
    + submission_window_days``. Fixed-date allocation is not supported in bulk mode.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        open_for_offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        slug (Union[Unset, str]):
        state (Union[Unset, list[CallStates]]):
        body (BulkRoundCreateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProtectedRound']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
            customer=customer,
            customer_keyword=customer_keyword,
            customer_uuid=customer_uuid,
            has_active_round=has_active_round,
            name=name,
            o=o,
            offering_uuid=offering_uuid,
            offerings_provider_uuid=offerings_provider_uuid,
            open_for_offering_uuid=open_for_offering_uuid,
            page=page,
            page_size=page_size,
            slug=slug,
            state=state,
        )
    ).parsed
