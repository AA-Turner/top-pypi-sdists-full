from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.group_membership_list_response import GroupMembershipListResponse
from ...models.list_group_memberships_sort import ListGroupMembershipsSort
from ...types import Unset


def _get_kwargs(
    *,
    filtergroup: None | str | Unset = UNSET,
    filteruser: None | str | Unset = UNSET,
    sort: ListGroupMembershipsSort | Unset = "created_at",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filtergroup: None | str | Unset
    if isinstance(filtergroup, Unset):
        json_filtergroup = UNSET
    else:
        json_filtergroup = filtergroup
    params["filter[group]"] = json_filtergroup

    json_filteruser: None | str | Unset
    if isinstance(filteruser, Unset):
        json_filteruser = UNSET
    else:
        json_filteruser = filteruser
    params["filter[user]"] = json_filteruser

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page[number]"] = pagenumber

    params["page[size]"] = pagesize

    params["meta[total]"] = metatotal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/group_memberships",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GroupMembershipListResponse | None:
    if response.status_code == 200:
        response_200 = GroupMembershipListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GroupMembershipListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filtergroup: None | str | Unset = UNSET,
    filteruser: None | str | Unset = UNSET,
    sort: ListGroupMembershipsSort | Unset = "created_at",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ErrorResponse | GroupMembershipListResponse]:
    """List Group Memberships

     List group memberships in the authenticated account. Pass `filter[group]` (a group key) to list
    members of a single group, or `filter[user]` (a UUID) to list a single user's memberships. The two
    filters may be combined to look up a specific (user, group) pair.

    Args:
        filtergroup (None | str | Unset): Group key to narrow the result to memberships in that
            group.
        filteruser (None | str | Unset): User UUID to narrow the result to memberships for that
            user.
        sort (ListGroupMembershipsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `created_at`. Allowed values: `created_at`, `-created_at`, `updated_at`,
            `-updated_at`. Default: 'created_at'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        filtergroup=filtergroup,
        filteruser=filteruser,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filtergroup: None | str | Unset = UNSET,
    filteruser: None | str | Unset = UNSET,
    sort: ListGroupMembershipsSort | Unset = "created_at",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ErrorResponse | GroupMembershipListResponse | None:
    """List Group Memberships

     List group memberships in the authenticated account. Pass `filter[group]` (a group key) to list
    members of a single group, or `filter[user]` (a UUID) to list a single user's memberships. The two
    filters may be combined to look up a specific (user, group) pair.

    Args:
        filtergroup (None | str | Unset): Group key to narrow the result to memberships in that
            group.
        filteruser (None | str | Unset): User UUID to narrow the result to memberships for that
            user.
        sort (ListGroupMembershipsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `created_at`. Allowed values: `created_at`, `-created_at`, `updated_at`,
            `-updated_at`. Default: 'created_at'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupMembershipListResponse
    """

    return sync_detailed(
        client=client,
        filtergroup=filtergroup,
        filteruser=filteruser,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filtergroup: None | str | Unset = UNSET,
    filteruser: None | str | Unset = UNSET,
    sort: ListGroupMembershipsSort | Unset = "created_at",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ErrorResponse | GroupMembershipListResponse]:
    """List Group Memberships

     List group memberships in the authenticated account. Pass `filter[group]` (a group key) to list
    members of a single group, or `filter[user]` (a UUID) to list a single user's memberships. The two
    filters may be combined to look up a specific (user, group) pair.

    Args:
        filtergroup (None | str | Unset): Group key to narrow the result to memberships in that
            group.
        filteruser (None | str | Unset): User UUID to narrow the result to memberships for that
            user.
        sort (ListGroupMembershipsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `created_at`. Allowed values: `created_at`, `-created_at`, `updated_at`,
            `-updated_at`. Default: 'created_at'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        filtergroup=filtergroup,
        filteruser=filteruser,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filtergroup: None | str | Unset = UNSET,
    filteruser: None | str | Unset = UNSET,
    sort: ListGroupMembershipsSort | Unset = "created_at",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ErrorResponse | GroupMembershipListResponse | None:
    """List Group Memberships

     List group memberships in the authenticated account. Pass `filter[group]` (a group key) to list
    members of a single group, or `filter[user]` (a UUID) to list a single user's memberships. The two
    filters may be combined to look up a specific (user, group) pair.

    Args:
        filtergroup (None | str | Unset): Group key to narrow the result to memberships in that
            group.
        filteruser (None | str | Unset): User UUID to narrow the result to memberships for that
            user.
        sort (ListGroupMembershipsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `created_at`. Allowed values: `created_at`, `-created_at`, `updated_at`,
            `-updated_at`. Default: 'created_at'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupMembershipListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filtergroup=filtergroup,
            filteruser=filteruser,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
