from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.schema_classes_paginated_list import SchemaClassesPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    schema_idsall_of: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/schema-classes".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(modified_at, Unset) and modified_at is not None:
        params["modifiedAt"] = modified_at
    if not isinstance(schema_idsall_of, Unset) and schema_idsall_of is not None:
        params["SchemaIds.allOf"] = schema_idsall_of

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[SchemaClassesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = SchemaClassesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[SchemaClassesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    schema_idsall_of: Union[Unset, str] = UNSET,
) -> Response[Union[SchemaClassesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        schema_idsall_of=schema_idsall_of,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    schema_idsall_of: Union[Unset, str] = UNSET,
) -> Optional[Union[SchemaClassesPaginatedList, BadRequestError]]:
    """ List schema classes """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        schema_idsall_of=schema_idsall_of,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    schema_idsall_of: Union[Unset, str] = UNSET,
) -> Response[Union[SchemaClassesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        modified_at=modified_at,
        schema_idsall_of=schema_idsall_of,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    modified_at: Union[Unset, str] = UNSET,
    schema_idsall_of: Union[Unset, str] = UNSET,
) -> Optional[Union[SchemaClassesPaginatedList, BadRequestError]]:
    """ List schema classes """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
            modified_at=modified_at,
            schema_idsall_of=schema_idsall_of,
        )
    ).parsed
