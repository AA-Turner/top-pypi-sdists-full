from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.requests_bulk_get import RequestsBulkGet
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    request_ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/requests:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(request_ids, Unset) and request_ids is not None:
        params["requestIds"] = request_ids
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[RequestsBulkGet, BadRequestError]]:
    if response.status_code == 200:
        response_200 = RequestsBulkGet.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RequestsBulkGet, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    request_ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[RequestsBulkGet, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        request_ids=request_ids,
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
    request_ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[RequestsBulkGet, BadRequestError]]:
    """ Bulk get Legacy Requests by API ID or display ID """

    return sync_detailed(
        client=client,
        request_ids=request_ids,
        display_ids=display_ids,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    request_ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[RequestsBulkGet, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        request_ids=request_ids,
        display_ids=display_ids,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    request_ids: Union[Unset, str] = UNSET,
    display_ids: Union[Unset, str] = UNSET,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[RequestsBulkGet, BadRequestError]]:
    """ Bulk get Legacy Requests by API ID or display ID """

    return (
        await asyncio_detailed(
            client=client,
            request_ids=request_ids,
            display_ids=display_ids,
            returning=returning,
        )
    ).parsed
