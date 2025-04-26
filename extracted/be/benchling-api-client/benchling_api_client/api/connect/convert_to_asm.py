from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.convert_to_asm import ConvertToASM
from ...models.convert_to_asm_response_200 import ConvertToASMResponse_200
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ConvertToASM,
) -> Dict[str, Any]:
    url = "{}/connect/convert-to-asm".format(client.base_url)

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
) -> Optional[Union[ConvertToASMResponse_200, BadRequestError]]:
    if response.status_code == 200:
        response_200 = ConvertToASMResponse_200.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ConvertToASMResponse_200, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ConvertToASM,
) -> Response[Union[ConvertToASMResponse_200, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: ConvertToASM,
) -> Optional[Union[ConvertToASMResponse_200, BadRequestError]]:
    """Converts an input blob or file containing instrument data to ASM (Allotrope Simple Model) JSON.

    May provide the name of the instrument vendor (see /connect/list-allotropy-vendors) or the ID of a
    connection associated with an instrument vendor.
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ConvertToASM,
) -> Response[Union[ConvertToASMResponse_200, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ConvertToASM,
) -> Optional[Union[ConvertToASMResponse_200, BadRequestError]]:
    """Converts an input blob or file containing instrument data to ASM (Allotrope Simple Model) JSON.

    May provide the name of the instrument vendor (see /connect/list-allotropy-vendors) or the ID of a
    connection associated with an instrument vendor.
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
