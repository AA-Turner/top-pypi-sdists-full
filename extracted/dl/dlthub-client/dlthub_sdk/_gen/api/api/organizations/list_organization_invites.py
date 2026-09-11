from http import HTTPStatus
from typing import Any, Literal
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.list_organization_invites_order_type_0_item import (
    ListOrganizationInvitesOrderType0Item,
)
from ...models.list_organization_invites_response_200 import (
    ListOrganizationInvitesResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort: list[Literal["date_added"]] | None | Unset = UNSET,
    order: list[ListOrganizationInvitesOrderType0Item] | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_sort: list[Literal["date_added"]] | None | Unset
    if isinstance(sort, Unset):
        json_sort = UNSET
    elif isinstance(sort, list):
        json_sort = sort

    else:
        json_sort = sort
    params["sort"] = json_sort

    json_order: list[str] | None | Unset
    if isinstance(order, Unset):
        json_order = UNSET
    elif isinstance(order, list):
        json_order = []
        for order_type_0_item_data in order:
            order_type_0_item = order_type_0_item_data.value
            json_order.append(order_type_0_item)

    else:
        json_order = order
    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/organizations/{organization_id}/invites".format(
            organization_id=quote(str(organization_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
    | None
):
    if response.status_code == 200:
        response_200 = ListOrganizationInvitesResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort: list[Literal["date_added"]] | None | Unset = UNSET,
    order: list[ListOrganizationInvitesOrderType0Item] | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
]:
    """ListOrganizationInvites

    Lists org-only invites for an organization.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        sort (list[Literal['date_added']] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListOrganizationInvitesOrderType0Item] | None | Unset): Sort directions, one
            per `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListOrganizationInvitesResponse200]
    """
    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        sort=sort,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort: list[Literal["date_added"]] | None | Unset = UNSET,
    order: list[ListOrganizationInvitesOrderType0Item] | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
    | None
):
    """ListOrganizationInvites

    Lists org-only invites for an organization.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        sort (list[Literal['date_added']] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListOrganizationInvitesOrderType0Item] | None | Unset): Sort directions, one
            per `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListOrganizationInvitesResponse200
    """
    return sync_detailed(
        organization_id=organization_id,
        client=client,
        limit=limit,
        offset=offset,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort: list[Literal["date_added"]] | None | Unset = UNSET,
    order: list[ListOrganizationInvitesOrderType0Item] | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
]:
    """ListOrganizationInvites

    Lists org-only invites for an organization.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        sort (list[Literal['date_added']] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListOrganizationInvitesOrderType0Item] | None | Unset): Sort directions, one
            per `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListOrganizationInvitesResponse200]
    """
    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    sort: list[Literal["date_added"]] | None | Unset = UNSET,
    order: list[ListOrganizationInvitesOrderType0Item] | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListOrganizationInvitesResponse200
    | None
):
    """ListOrganizationInvites

    Lists org-only invites for an organization.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        sort (list[Literal['date_added']] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListOrganizationInvitesOrderType0Item] | None | Unset): Sort directions, one
            per `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListOrganizationInvitesResponse200
    """
    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            limit=limit,
            offset=offset,
            sort=sort,
            order=order,
        )
    ).parsed
