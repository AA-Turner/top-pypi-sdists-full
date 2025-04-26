import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_sessions_paginated_list import AppSessionsPaginatedList
from ...models.bad_request_error import BadRequestError
from ...models.list_app_sessions_sort import ListAppSessionsSort
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppSessionsSort] = ListAppSessionsSort.MODIFIEDAT,
    created_atlt: Union[Unset, datetime.datetime] = UNSET,
    created_atgt: Union[Unset, datetime.datetime] = UNSET,
    created_atlte: Union[Unset, datetime.datetime] = UNSET,
    created_atgte: Union[Unset, datetime.datetime] = UNSET,
    modified_atlt: Union[Unset, datetime.datetime] = UNSET,
    modified_atgt: Union[Unset, datetime.datetime] = UNSET,
    modified_atlte: Union[Unset, datetime.datetime] = UNSET,
    modified_atgte: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/app-sessions".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    json_created_atlt: Union[Unset, str] = UNSET
    if not isinstance(created_atlt, Unset):
        json_created_atlt = created_atlt.isoformat()

    json_created_atgt: Union[Unset, str] = UNSET
    if not isinstance(created_atgt, Unset):
        json_created_atgt = created_atgt.isoformat()

    json_created_atlte: Union[Unset, str] = UNSET
    if not isinstance(created_atlte, Unset):
        json_created_atlte = created_atlte.isoformat()

    json_created_atgte: Union[Unset, str] = UNSET
    if not isinstance(created_atgte, Unset):
        json_created_atgte = created_atgte.isoformat()

    json_modified_atlt: Union[Unset, str] = UNSET
    if not isinstance(modified_atlt, Unset):
        json_modified_atlt = modified_atlt.isoformat()

    json_modified_atgt: Union[Unset, str] = UNSET
    if not isinstance(modified_atgt, Unset):
        json_modified_atgt = modified_atgt.isoformat()

    json_modified_atlte: Union[Unset, str] = UNSET
    if not isinstance(modified_atlte, Unset):
        json_modified_atlte = modified_atlte.isoformat()

    json_modified_atgte: Union[Unset, str] = UNSET
    if not isinstance(modified_atgte, Unset):
        json_modified_atgte = modified_atgte.isoformat()

    params: Dict[str, Any] = {}
    if not isinstance(app_id, Unset) and app_id is not None:
        params["appId"] = app_id
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(json_created_atlt, Unset) and json_created_atlt is not None:
        params["createdAt.lt"] = json_created_atlt
    if not isinstance(json_created_atgt, Unset) and json_created_atgt is not None:
        params["createdAt.gt"] = json_created_atgt
    if not isinstance(json_created_atlte, Unset) and json_created_atlte is not None:
        params["createdAt.lte"] = json_created_atlte
    if not isinstance(json_created_atgte, Unset) and json_created_atgte is not None:
        params["createdAt.gte"] = json_created_atgte
    if not isinstance(json_modified_atlt, Unset) and json_modified_atlt is not None:
        params["modifiedAt.lt"] = json_modified_atlt
    if not isinstance(json_modified_atgt, Unset) and json_modified_atgt is not None:
        params["modifiedAt.gt"] = json_modified_atgt
    if not isinstance(json_modified_atlte, Unset) and json_modified_atlte is not None:
        params["modifiedAt.lte"] = json_modified_atlte
    if not isinstance(json_modified_atgte, Unset) and json_modified_atgte is not None:
        params["modifiedAt.gte"] = json_modified_atgte
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
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
) -> Optional[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AppSessionsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
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
    sort: Union[Unset, ListAppSessionsSort] = ListAppSessionsSort.MODIFIEDAT,
    created_atlt: Union[Unset, datetime.datetime] = UNSET,
    created_atgt: Union[Unset, datetime.datetime] = UNSET,
    created_atlte: Union[Unset, datetime.datetime] = UNSET,
    created_atgte: Union[Unset, datetime.datetime] = UNSET,
    modified_atlt: Union[Unset, datetime.datetime] = UNSET,
    modified_atgt: Union[Unset, datetime.datetime] = UNSET,
    modified_atlte: Union[Unset, datetime.datetime] = UNSET,
    modified_atgte: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        next_token=next_token,
        page_size=page_size,
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
    sort: Union[Unset, ListAppSessionsSort] = ListAppSessionsSort.MODIFIEDAT,
    created_atlt: Union[Unset, datetime.datetime] = UNSET,
    created_atgt: Union[Unset, datetime.datetime] = UNSET,
    created_atlte: Union[Unset, datetime.datetime] = UNSET,
    created_atgte: Union[Unset, datetime.datetime] = UNSET,
    modified_atlt: Union[Unset, datetime.datetime] = UNSET,
    modified_atgt: Union[Unset, datetime.datetime] = UNSET,
    modified_atlte: Union[Unset, datetime.datetime] = UNSET,
    modified_atgte: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
    """ List all app sessions """

    return sync_detailed(
        client=client,
        app_id=app_id,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        next_token=next_token,
        page_size=page_size,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppSessionsSort] = ListAppSessionsSort.MODIFIEDAT,
    created_atlt: Union[Unset, datetime.datetime] = UNSET,
    created_atgt: Union[Unset, datetime.datetime] = UNSET,
    created_atlte: Union[Unset, datetime.datetime] = UNSET,
    created_atgte: Union[Unset, datetime.datetime] = UNSET,
    modified_atlt: Union[Unset, datetime.datetime] = UNSET,
    modified_atgt: Union[Unset, datetime.datetime] = UNSET,
    modified_atlte: Union[Unset, datetime.datetime] = UNSET,
    modified_atgte: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        next_token=next_token,
        page_size=page_size,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    app_id: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListAppSessionsSort] = ListAppSessionsSort.MODIFIEDAT,
    created_atlt: Union[Unset, datetime.datetime] = UNSET,
    created_atgt: Union[Unset, datetime.datetime] = UNSET,
    created_atlte: Union[Unset, datetime.datetime] = UNSET,
    created_atgte: Union[Unset, datetime.datetime] = UNSET,
    modified_atlt: Union[Unset, datetime.datetime] = UNSET,
    modified_atgt: Union[Unset, datetime.datetime] = UNSET,
    modified_atlte: Union[Unset, datetime.datetime] = UNSET,
    modified_atgte: Union[Unset, datetime.datetime] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppSessionsPaginatedList, BadRequestError, NotFoundError]]:
    """ List all app sessions """

    return (
        await asyncio_detailed(
            client=client,
            app_id=app_id,
            sort=sort,
            created_atlt=created_atlt,
            created_atgt=created_atgt,
            created_atlte=created_atlte,
            created_atgte=created_atgte,
            modified_atlt=modified_atlt,
            modified_atgt=modified_atgt,
            modified_atlte=modified_atlte,
            modified_atgte=modified_atgte,
            next_token=next_token,
            page_size=page_size,
            returning=returning,
        )
    ).parsed
