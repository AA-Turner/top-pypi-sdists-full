from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.app_session import AppSession
from ...models.app_session_update import AppSessionUpdate
from ...models.bad_request_error import BadRequestError
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    id: str,
    json_body: AppSessionUpdate,
) -> Dict[str, Any]:
    url = "{}/app-sessions/{id}".format(client.base_url, id=id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AppSession.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: str,
    json_body: AppSessionUpdate,
) -> Response[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: str,
    json_body: AppSessionUpdate,
) -> Optional[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update app session """

    return sync_detailed(
        client=client,
        id=id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: str,
    json_body: AppSessionUpdate,
) -> Response[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        id=id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: str,
    json_body: AppSessionUpdate,
) -> Optional[Union[AppSession, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update app session """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            json_body=json_body,
        )
    ).parsed
