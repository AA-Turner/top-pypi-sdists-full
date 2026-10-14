from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_definition_state_enum import MetricDefinitionStateEnum
from ...models.metric_kind_enum import MetricKindEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_global"] = is_global

    params["key"] = key

    json_kind: Union[Unset, str] = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params["name"] = name

    json_owner_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(owner_customer_uuid, Unset):
        json_owner_customer_uuid = str(owner_customer_uuid)
    params["owner_customer_uuid"] = json_owner_customer_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-metric-definitions/",
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
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            is_global=is_global,
            key=key,
            kind=kind,
            name=name,
            owner_customer_uuid=owner_customer_uuid,
            page=page,
            page_size=page_size,
            state=state,
        )
    ).parsed
