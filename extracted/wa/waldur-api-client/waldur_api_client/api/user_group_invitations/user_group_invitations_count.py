from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_req_o_enum import BackendResourceReqOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["is_active"] = is_active

    params["is_public"] = is_public

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["role_name"] = role_name

    json_role_uuid: Union[Unset, str] = UNSET
    if not isinstance(role_uuid, Unset):
        json_role_uuid = str(role_uuid)
    params["role_uuid"] = json_role_uuid

    params["scope"] = scope

    params["scope_type"] = scope_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/user-group-invitations/",
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
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List group invitations

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> int:
    """List group invitations

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List group invitations

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        is_active=is_active,
        is_public=is_public,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_type=scope_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
) -> int:
    """List group invitations

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        is_public (Union[Unset, bool]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            is_active=is_active,
            is_public=is_public,
            o=o,
            page=page,
            page_size=page_size,
            role_name=role_name,
            role_uuid=role_uuid,
            scope=scope,
            scope_type=scope_type,
        )
    ).parsed
