from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.get_user_warehouse_logins_response_200 import GetUserWarehouseLoginsResponse_200
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    user_id: str,
) -> Dict[str, Any]:
    url = "{}/users/{user_id}/warehouse-credentials".format(client.base_url, user_id=user_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    if response.status_code == 200:
        response_200 = GetUserWarehouseLoginsResponse_200.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    user_id: str,
) -> Response[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    user_id: str,
) -> Optional[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    """ Returns the list of warehouse credential summaries for this user. """

    return sync_detailed(
        client=client,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    user_id: str,
) -> Response[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        user_id=user_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    user_id: str,
) -> Optional[Union[GetUserWarehouseLoginsResponse_200, NotFoundError]]:
    """ Returns the list of warehouse credential summaries for this user. """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
        )
    ).parsed
