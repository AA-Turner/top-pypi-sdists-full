from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.instrument_query import InstrumentQuery
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    instrument_query_id: str,
) -> Dict[str, Any]:
    url = "{}/instruments/{instrument_query_id}/query".format(
        client.base_url, instrument_query_id=instrument_query_id
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
) -> Optional[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = InstrumentQuery.from_dict(response.json(), strict=False)

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
) -> Response[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    instrument_query_id: str,
) -> Response[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        instrument_query_id=instrument_query_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    instrument_query_id: str,
) -> Optional[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    """ Get an instrument query """

    return sync_detailed(
        client=client,
        instrument_query_id=instrument_query_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    instrument_query_id: str,
) -> Response[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        instrument_query_id=instrument_query_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    instrument_query_id: str,
) -> Optional[Union[InstrumentQuery, BadRequestError, NotFoundError]]:
    """ Get an instrument query """

    return (
        await asyncio_detailed(
            client=client,
            instrument_query_id=instrument_query_id,
        )
    ).parsed
