from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_canvas import AppCanvas
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    canvas_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/app-canvases/{canvas_id}".format(client.base_url, canvas_id=canvas_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AppCanvas, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AppCanvas.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AppCanvas, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    canvas_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppCanvas, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        canvas_id=canvas_id,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    canvas_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppCanvas, NotFoundError]]:
    """ Get the current state of the App Canvas, including user input elements. """

    return sync_detailed(
        client=client,
        canvas_id=canvas_id,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    canvas_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[AppCanvas, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        canvas_id=canvas_id,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    canvas_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[AppCanvas, NotFoundError]]:
    """ Get the current state of the App Canvas, including user input elements. """

    return (
        await asyncio_detailed(
            client=client,
            canvas_id=canvas_id,
            returning=returning,
        )
    ).parsed
