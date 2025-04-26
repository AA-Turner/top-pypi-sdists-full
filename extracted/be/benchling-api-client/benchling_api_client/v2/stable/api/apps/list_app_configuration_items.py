from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_configuration_paginated_list import AppConfigurationPaginatedList
from ...models.list_app_configuration_items_sort import ListAppConfigurationItemsSort
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    app_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppConfigurationItemsSort] = ListAppConfigurationItemsSort.MODIFIEDATDESC,
) -> Dict[str, Any]:
    url = "{}/app-configuration-items".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(modified_at, Unset) and modified_at is not None:
        params["modifiedAt"] = modified_at
    if not isinstance(app_id, Unset) and app_id is not None:
        params["appId"] = app_id
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AppConfigurationPaginatedList, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AppConfigurationPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AppConfigurationPaginatedList, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    app_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppConfigurationItemsSort] = ListAppConfigurationItemsSort.MODIFIEDATDESC,
) -> Response[Union[AppConfigurationPaginatedList, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        app_id=app_id,
        ids=ids,
        sort=sort,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    app_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppConfigurationItemsSort] = ListAppConfigurationItemsSort.MODIFIEDATDESC,
) -> Optional[Union[AppConfigurationPaginatedList, NotFoundError]]:
    """ Get app configuration items """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        app_id=app_id,
        ids=ids,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    app_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppConfigurationItemsSort] = ListAppConfigurationItemsSort.MODIFIEDATDESC,
) -> Response[Union[AppConfigurationPaginatedList, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        app_id=app_id,
        ids=ids,
        sort=sort,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    app_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppConfigurationItemsSort] = ListAppConfigurationItemsSort.MODIFIEDATDESC,
) -> Optional[Union[AppConfigurationPaginatedList, NotFoundError]]:
    """ Get app configuration items """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
            modified_at=modified_at,
            app_id=app_id,
            ids=ids,
            sort=sort,
        )
    ).parsed
