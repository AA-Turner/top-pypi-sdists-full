from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_canvases_paginated_list import AppCanvasesPaginatedList
from ...models.bad_request_error import BadRequestError
from ...models.list_app_canvases_enabled import ListAppCanvasesEnabled
from ...models.list_app_canvases_sort import ListAppCanvasesSort
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    feature_id: Union[Unset, str] = UNSET,
    resource_id: Union[Unset, str] = UNSET,
    enabled: Union[Unset, ListAppCanvasesEnabled] = UNSET,
    archive_reason: Union[Unset, str] = "NOT_ARCHIVED",
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppCanvasesSort] = ListAppCanvasesSort.MODIFIEDATDESC,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/app-canvases".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_enabled: Union[Unset, int] = UNSET
    if not isinstance(enabled, Unset):
        json_enabled = enabled.value

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(app_id, Unset) and app_id is not None:
        params["appId"] = app_id
    if not isinstance(feature_id, Unset) and feature_id is not None:
        params["featureId"] = feature_id
    if not isinstance(resource_id, Unset) and resource_id is not None:
        params["resourceId"] = resource_id
    if not isinstance(json_enabled, Unset) and json_enabled is not None:
        params["enabled"] = json_enabled
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AppCanvasesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = AppCanvasesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AppCanvasesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    feature_id: Union[Unset, str] = UNSET,
    resource_id: Union[Unset, str] = UNSET,
    enabled: Union[Unset, ListAppCanvasesEnabled] = UNSET,
    archive_reason: Union[Unset, str] = "NOT_ARCHIVED",
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppCanvasesSort] = ListAppCanvasesSort.MODIFIEDATDESC,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppCanvasesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
        feature_id=feature_id,
        resource_id=resource_id,
        enabled=enabled,
        archive_reason=archive_reason,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    feature_id: Union[Unset, str] = UNSET,
    resource_id: Union[Unset, str] = UNSET,
    enabled: Union[Unset, ListAppCanvasesEnabled] = UNSET,
    archive_reason: Union[Unset, str] = "NOT_ARCHIVED",
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppCanvasesSort] = ListAppCanvasesSort.MODIFIEDATDESC,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppCanvasesPaginatedList, BadRequestError]]:
    """ List app canvases """

    return sync_detailed(
        client=client,
        app_id=app_id,
        feature_id=feature_id,
        resource_id=resource_id,
        enabled=enabled,
        archive_reason=archive_reason,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    feature_id: Union[Unset, str] = UNSET,
    resource_id: Union[Unset, str] = UNSET,
    enabled: Union[Unset, ListAppCanvasesEnabled] = UNSET,
    archive_reason: Union[Unset, str] = "NOT_ARCHIVED",
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppCanvasesSort] = ListAppCanvasesSort.MODIFIEDATDESC,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppCanvasesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
        feature_id=feature_id,
        resource_id=resource_id,
        enabled=enabled,
        archive_reason=archive_reason,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    feature_id: Union[Unset, str] = UNSET,
    resource_id: Union[Unset, str] = UNSET,
    enabled: Union[Unset, ListAppCanvasesEnabled] = UNSET,
    archive_reason: Union[Unset, str] = "NOT_ARCHIVED",
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppCanvasesSort] = ListAppCanvasesSort.MODIFIEDATDESC,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppCanvasesPaginatedList, BadRequestError]]:
    """ List app canvases """

    return (
        await asyncio_detailed(
            client=client,
            app_id=app_id,
            feature_id=feature_id,
            resource_id=resource_id,
            enabled=enabled,
            archive_reason=archive_reason,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            returning=returning,
        )
    ).parsed
