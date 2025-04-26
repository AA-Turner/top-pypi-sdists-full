from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_oligo import DnaOligo
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    oligo_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/oligos/{oligo_id}".format(client.base_url, oligo_id=oligo_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaOligo, BadRequestError]]:
    if response.status_code == 200:
        response_200 = DnaOligo.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaOligo, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    oligo_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[DnaOligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    oligo_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[DnaOligo, BadRequestError]]:
    """ Get an Oligo """

    return sync_detailed(
        client=client,
        oligo_id=oligo_id,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    oligo_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[DnaOligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    oligo_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[DnaOligo, BadRequestError]]:
    """ Get an Oligo """

    return (
        await asyncio_detailed(
            client=client,
            oligo_id=oligo_id,
            returning=returning,
        )
    ).parsed
