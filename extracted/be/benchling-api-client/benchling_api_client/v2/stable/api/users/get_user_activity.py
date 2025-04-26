from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...models.user_activity import UserActivity
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    user_id: str,
) -> Dict[str, Any]:
    url = "{}/users/{user_id}/activity".format(client.base_url, user_id=user_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[UserActivity, NotFoundError]]:
    if response.status_code == 200:
        response_200 = UserActivity.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[UserActivity, NotFoundError]]:
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
) -> Response[Union[UserActivity, NotFoundError]]:
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
) -> Optional[Union[UserActivity, NotFoundError]]:
    """Returns activity metadata for a specific user by ID. This currently includes lastSeen data."""

    return sync_detailed(
        client=client,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    user_id: str,
) -> Response[Union[UserActivity, NotFoundError]]:
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
) -> Optional[Union[UserActivity, NotFoundError]]:
    """Returns activity metadata for a specific user by ID. This currently includes lastSeen data."""

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
        )
    ).parsed
