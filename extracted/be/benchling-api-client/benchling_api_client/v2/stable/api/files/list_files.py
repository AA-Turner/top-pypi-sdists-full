from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.files_paginated_list import FilesPaginatedList
from ...models.listing_error import ListingError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/files".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(display_ids, Unset) and display_ids is not None:
        params["displayIds"] = display_ids
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[FilesPaginatedList, ListingError]]:
    if response.status_code == 200:
        response_200 = FilesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = ListingError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[FilesPaginatedList, ListingError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[FilesPaginatedList, ListingError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        display_ids=display_ids,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[FilesPaginatedList, ListingError]]:
    """ List files """

    return sync_detailed(
        client=client,
        ids=ids,
        display_ids=display_ids,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[FilesPaginatedList, ListingError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        display_ids=display_ids,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[FilesPaginatedList, ListingError]]:
    """ List files """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
            display_ids=display_ids,
            returning=returning,
        )
    ).parsed
