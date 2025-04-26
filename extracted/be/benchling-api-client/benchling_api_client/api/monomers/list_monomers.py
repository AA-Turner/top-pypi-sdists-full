from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.monomers_paginated_list import MonomersPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/monomers".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[MonomersPaginatedList]:
    if response.status_code == 200:
        response_200 = MonomersPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[MonomersPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[MonomersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[MonomersPaginatedList]:
    """ List all available monomers """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[MonomersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[MonomersPaginatedList]:
    """ List all available monomers """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            returning=returning,
        )
    ).parsed
