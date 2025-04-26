from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.forbidden_error import ForbiddenError
from ...models.monomer import Monomer
from ...models.monomer_update import MonomerUpdate
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    monomer_id: str,
    json_body: MonomerUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/monomers/{monomer_id}".format(client.base_url, monomer_id=monomer_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Monomer.from_dict(response.json(), strict=False)

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
) -> Response[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    monomer_id: str,
    json_body: MonomerUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        monomer_id=monomer_id,
        json_body=json_body,
        returning=returning,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    monomer_id: str,
    json_body: MonomerUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update a Monomer. """

    return sync_detailed(
        client=client,
        monomer_id=monomer_id,
        json_body=json_body,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    monomer_id: str,
    json_body: MonomerUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        monomer_id=monomer_id,
        json_body=json_body,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    monomer_id: str,
    json_body: MonomerUpdate,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[Monomer, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update a Monomer. """

    return (
        await asyncio_detailed(
            client=client,
            monomer_id=monomer_id,
            json_body=json_body,
            returning=returning,
        )
    ).parsed
