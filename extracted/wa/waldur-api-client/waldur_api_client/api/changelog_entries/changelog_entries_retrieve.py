from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.changelog_entry_list import ChangelogEntryList
from ...models.changelog_entry_list_category_enum import ChangelogEntryListCategoryEnum
from ...models.changelog_entry_list_o_enum import ChangelogEntryListOEnum
from ...models.changelog_entry_list_risk_enum import ChangelogEntryListRiskEnum
from ...models.changelog_entry_list_scope_enum import ChangelogEntryListScopeEnum
from ...models.changelog_entry_list_type_enum import ChangelogEntryListTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    category: Union[Unset, ChangelogEntryListCategoryEnum] = UNSET,
    highlight: Union[Unset, bool] = UNSET,
    o: Union[Unset, ChangelogEntryListOEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release: Union[Unset, str] = UNSET,
    relevant_only: Union[Unset, bool] = UNSET,
    risk: Union[Unset, ChangelogEntryListRiskEnum] = UNSET,
    scope: Union[Unset, ChangelogEntryListScopeEnum] = UNSET,
    search: Union[Unset, str] = UNSET,
    type_: Union[Unset, ChangelogEntryListTypeEnum] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_category: Union[Unset, str] = UNSET
    if not isinstance(category, Unset):
        json_category = category.value

    params["category"] = json_category

    params["highlight"] = highlight

    json_o: Union[Unset, str] = UNSET
    if not isinstance(o, Unset):
        json_o = o.value

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["release"] = release

    params["relevant_only"] = relevant_only

    json_risk: Union[Unset, str] = UNSET
    if not isinstance(risk, Unset):
        json_risk = risk.value

    params["risk"] = json_risk

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["search"] = search

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/changelog-entries/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ChangelogEntryList:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChangelogEntryList.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChangelogEntryList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, ChangelogEntryListCategoryEnum] = UNSET,
    highlight: Union[Unset, bool] = UNSET,
    o: Union[Unset, ChangelogEntryListOEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release: Union[Unset, str] = UNSET,
    relevant_only: Union[Unset, bool] = UNSET,
    risk: Union[Unset, ChangelogEntryListRiskEnum] = UNSET,
    scope: Union[Unset, ChangelogEntryListScopeEnum] = UNSET,
    search: Union[Unset, str] = UNSET,
    type_: Union[Unset, ChangelogEntryListTypeEnum] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[ChangelogEntryList]:
    """List changelog entries

     Returns a flat, paginated list of changelog entries for all pending versions, or, with `release`,
    the entries that release introduced. Supports filtering by type, risk, scope, version, and text
    search. Compatible with the standard Waldur table component.

    Args:
        category (Union[Unset, ChangelogEntryListCategoryEnum]):
        highlight (Union[Unset, bool]):
        o (Union[Unset, ChangelogEntryListOEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release (Union[Unset, str]):
        relevant_only (Union[Unset, bool]):
        risk (Union[Unset, ChangelogEntryListRiskEnum]):
        scope (Union[Unset, ChangelogEntryListScopeEnum]):
        search (Union[Unset, str]):
        type_ (Union[Unset, ChangelogEntryListTypeEnum]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogEntryList]
    """

    kwargs = _get_kwargs(
        category=category,
        highlight=highlight,
        o=o,
        page=page,
        page_size=page_size,
        release=release,
        relevant_only=relevant_only,
        risk=risk,
        scope=scope,
        search=search,
        type_=type_,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, ChangelogEntryListCategoryEnum] = UNSET,
    highlight: Union[Unset, bool] = UNSET,
    o: Union[Unset, ChangelogEntryListOEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release: Union[Unset, str] = UNSET,
    relevant_only: Union[Unset, bool] = UNSET,
    risk: Union[Unset, ChangelogEntryListRiskEnum] = UNSET,
    scope: Union[Unset, ChangelogEntryListScopeEnum] = UNSET,
    search: Union[Unset, str] = UNSET,
    type_: Union[Unset, ChangelogEntryListTypeEnum] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> ChangelogEntryList:
    """List changelog entries

     Returns a flat, paginated list of changelog entries for all pending versions, or, with `release`,
    the entries that release introduced. Supports filtering by type, risk, scope, version, and text
    search. Compatible with the standard Waldur table component.

    Args:
        category (Union[Unset, ChangelogEntryListCategoryEnum]):
        highlight (Union[Unset, bool]):
        o (Union[Unset, ChangelogEntryListOEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release (Union[Unset, str]):
        relevant_only (Union[Unset, bool]):
        risk (Union[Unset, ChangelogEntryListRiskEnum]):
        scope (Union[Unset, ChangelogEntryListScopeEnum]):
        search (Union[Unset, str]):
        type_ (Union[Unset, ChangelogEntryListTypeEnum]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogEntryList
    """

    return sync_detailed(
        client=client,
        category=category,
        highlight=highlight,
        o=o,
        page=page,
        page_size=page_size,
        release=release,
        relevant_only=relevant_only,
        risk=risk,
        scope=scope,
        search=search,
        type_=type_,
        version=version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, ChangelogEntryListCategoryEnum] = UNSET,
    highlight: Union[Unset, bool] = UNSET,
    o: Union[Unset, ChangelogEntryListOEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release: Union[Unset, str] = UNSET,
    relevant_only: Union[Unset, bool] = UNSET,
    risk: Union[Unset, ChangelogEntryListRiskEnum] = UNSET,
    scope: Union[Unset, ChangelogEntryListScopeEnum] = UNSET,
    search: Union[Unset, str] = UNSET,
    type_: Union[Unset, ChangelogEntryListTypeEnum] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[ChangelogEntryList]:
    """List changelog entries

     Returns a flat, paginated list of changelog entries for all pending versions, or, with `release`,
    the entries that release introduced. Supports filtering by type, risk, scope, version, and text
    search. Compatible with the standard Waldur table component.

    Args:
        category (Union[Unset, ChangelogEntryListCategoryEnum]):
        highlight (Union[Unset, bool]):
        o (Union[Unset, ChangelogEntryListOEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release (Union[Unset, str]):
        relevant_only (Union[Unset, bool]):
        risk (Union[Unset, ChangelogEntryListRiskEnum]):
        scope (Union[Unset, ChangelogEntryListScopeEnum]):
        search (Union[Unset, str]):
        type_ (Union[Unset, ChangelogEntryListTypeEnum]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogEntryList]
    """

    kwargs = _get_kwargs(
        category=category,
        highlight=highlight,
        o=o,
        page=page,
        page_size=page_size,
        release=release,
        relevant_only=relevant_only,
        risk=risk,
        scope=scope,
        search=search,
        type_=type_,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, ChangelogEntryListCategoryEnum] = UNSET,
    highlight: Union[Unset, bool] = UNSET,
    o: Union[Unset, ChangelogEntryListOEnum] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    release: Union[Unset, str] = UNSET,
    relevant_only: Union[Unset, bool] = UNSET,
    risk: Union[Unset, ChangelogEntryListRiskEnum] = UNSET,
    scope: Union[Unset, ChangelogEntryListScopeEnum] = UNSET,
    search: Union[Unset, str] = UNSET,
    type_: Union[Unset, ChangelogEntryListTypeEnum] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> ChangelogEntryList:
    """List changelog entries

     Returns a flat, paginated list of changelog entries for all pending versions, or, with `release`,
    the entries that release introduced. Supports filtering by type, risk, scope, version, and text
    search. Compatible with the standard Waldur table component.

    Args:
        category (Union[Unset, ChangelogEntryListCategoryEnum]):
        highlight (Union[Unset, bool]):
        o (Union[Unset, ChangelogEntryListOEnum]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        release (Union[Unset, str]):
        relevant_only (Union[Unset, bool]):
        risk (Union[Unset, ChangelogEntryListRiskEnum]):
        scope (Union[Unset, ChangelogEntryListScopeEnum]):
        search (Union[Unset, str]):
        type_ (Union[Unset, ChangelogEntryListTypeEnum]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogEntryList
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
            highlight=highlight,
            o=o,
            page=page,
            page_size=page_size,
            release=release,
            relevant_only=relevant_only,
            risk=risk,
            scope=scope,
            search=search,
            type_=type_,
            version=version,
        )
    ).parsed
