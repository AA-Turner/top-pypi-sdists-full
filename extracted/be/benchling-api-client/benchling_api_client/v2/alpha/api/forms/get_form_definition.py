from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.form_definition import FormDefinition
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    form_definition_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/form-definitions/{form_definition_id}".format(
        client.base_url, form_definition_id=form_definition_id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[FormDefinition, None]]:
    if response.status_code == 200:
        response_200 = FormDefinition.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[FormDefinition, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    form_definition_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[FormDefinition, None]]:
    kwargs = _get_kwargs(
        client=client,
        form_definition_id=form_definition_id,
        returning=returning,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    form_definition_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[FormDefinition, None]]:
    """Get a specific form definition. Only the latest version is returned"""

    return sync_detailed(
        client=client,
        form_definition_id=form_definition_id,
        returning=returning,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    form_definition_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Response[Union[FormDefinition, None]]:
    kwargs = _get_kwargs(
        client=client,
        form_definition_id=form_definition_id,
        returning=returning,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    form_definition_id: str,
    returning: Union[Unset, str] = UNSET,
) -> Optional[Union[FormDefinition, None]]:
    """Get a specific form definition. Only the latest version is returned"""

    return (
        await asyncio_detailed(
            client=client,
            form_definition_id=form_definition_id,
            returning=returning,
        )
    ).parsed
