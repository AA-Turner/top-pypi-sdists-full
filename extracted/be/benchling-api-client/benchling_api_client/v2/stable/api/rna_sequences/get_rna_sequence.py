from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.rna_sequence import RnaSequence
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    rna_sequence_id: str,
    returning: Union[Unset, str] = UNSET,
    custom_notation_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rna-sequences/{rna_sequence_id}".format(client.base_url, rna_sequence_id=rna_sequence_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning
    if not isinstance(custom_notation_id, Unset) and custom_notation_id is not None:
        params["customNotationId"] = custom_notation_id

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[RnaSequence, BadRequestError]]:
    if response.status_code == 200:
        response_200 = RnaSequence.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RnaSequence, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    rna_sequence_id: str,
    returning: Union[Unset, str] = UNSET,
    custom_notation_id: Union[Unset, str] = UNSET,
) -> Response[Union[RnaSequence, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        rna_sequence_id=rna_sequence_id,
        returning=returning,
        custom_notation_id=custom_notation_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    rna_sequence_id: str,
    returning: Union[Unset, str] = UNSET,
    custom_notation_id: Union[Unset, str] = UNSET,
) -> Optional[Union[RnaSequence, BadRequestError]]:
    """ Get an RNA sequence """

    return sync_detailed(
        client=client,
        rna_sequence_id=rna_sequence_id,
        returning=returning,
        custom_notation_id=custom_notation_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    rna_sequence_id: str,
    returning: Union[Unset, str] = UNSET,
    custom_notation_id: Union[Unset, str] = UNSET,
) -> Response[Union[RnaSequence, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        rna_sequence_id=rna_sequence_id,
        returning=returning,
        custom_notation_id=custom_notation_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    rna_sequence_id: str,
    returning: Union[Unset, str] = UNSET,
    custom_notation_id: Union[Unset, str] = UNSET,
) -> Optional[Union[RnaSequence, BadRequestError]]:
    """ Get an RNA sequence """

    return (
        await asyncio_detailed(
            client=client,
            rna_sequence_id=rna_sequence_id,
            returning=returning,
            custom_notation_id=custom_notation_id,
        )
    ).parsed
