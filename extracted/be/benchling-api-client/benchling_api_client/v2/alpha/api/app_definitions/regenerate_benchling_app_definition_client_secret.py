from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_client_secret import AppClientSecret
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    app_def_id: str,
) -> Dict[str, Any]:
    url = "{}/app-definitions/{app_def_id}/generate-oauth2-client-secret".format(
        client.base_url, app_def_id=app_def_id
    )

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
) -> Optional[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AppClientSecret.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    app_def_id: str,
) -> Response[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        app_def_id=app_def_id,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    app_def_id: str,
) -> Optional[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    """ Regenerate the oauth2 client key for the given app definition. Note that this will invalidate the previous key, and the value returned by this call can't be retrieved from Benchling. """

    return sync_detailed(
        client=client,
        app_def_id=app_def_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    app_def_id: str,
) -> Response[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        app_def_id=app_def_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    app_def_id: str,
) -> Optional[Union[AppClientSecret, ForbiddenError, NotFoundError]]:
    """ Regenerate the oauth2 client key for the given app definition. Note that this will invalidate the previous key, and the value returned by this call can't be retrieved from Benchling. """

    return (
        await asyncio_detailed(
            client=client,
            app_def_id=app_def_id,
        )
    ).parsed
