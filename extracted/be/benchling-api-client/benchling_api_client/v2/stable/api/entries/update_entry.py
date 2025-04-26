from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.entry import Entry
from ...models.entry_update import EntryUpdate
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/entries/{entry_id}".format(client.base_url, entry_id=entry_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Entry]:
    if response.status_code == 200:
        response_200 = Entry.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Entry]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Response[Entry]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
        returning=returning,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Entry]:
    """ Update a notebook entry's metadata """

    return sync_detailed(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Response[Entry]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        json_body=json_body,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    entry_id: str,
    json_body: EntryUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Entry]:
    """ Update a notebook entry's metadata """

    return (
        await asyncio_detailed(
            client=client,
            entry_id=entry_id,
            json_body=json_body,
            returning=returning,
        )
    ).parsed
