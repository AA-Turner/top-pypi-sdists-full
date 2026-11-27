import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_tokens_as_super_admin_flag import ListTokensAsSuperAdminFlag
from ...models.list_tokens_as_super_admin_response_200_item import ListTokensAsSuperAdminResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    flag: Union[Unset, None, ListTokensAsSuperAdminFlag] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_last_used_at: Union[Unset, None, datetime.datetime] = UNSET,
    after_token_prefix: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_flag: Union[Unset, None, str] = UNSET
    if not isinstance(flag, Unset):
        json_flag = flag.value if flag else None

    params["flag"] = json_flag

    params["search"] = search

    params["per_page"] = per_page

    json_after_last_used_at: Union[Unset, None, str] = UNSET
    if not isinstance(after_last_used_at, Unset):
        json_after_last_used_at = after_last_used_at.isoformat() if after_last_used_at else None

    params["after_last_used_at"] = json_after_last_used_at

    params["after_token_prefix"] = after_token_prefix

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/users/tokens/list_as_super_admin",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListTokensAsSuperAdminResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListTokensAsSuperAdminResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListTokensAsSuperAdminResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    flag: Union[Unset, None, ListTokensAsSuperAdminFlag] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_last_used_at: Union[Unset, None, datetime.datetime] = UNSET,
    after_token_prefix: Union[Unset, None, str] = UNSET,
) -> Response[List["ListTokensAsSuperAdminResponse200Item"]]:
    """list every user's tokens, least recently used first (superadmin only, EE)

     Tokens the server expires or renews on its own are left out. Pages are read with a cursor: pass the
    last row's `last_used_at` and `token_prefix` to get the next page.

    Args:
        flag (Union[Unset, None, ListTokensAsSuperAdminFlag]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        after_last_used_at (Union[Unset, None, datetime.datetime]):
        after_token_prefix (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListTokensAsSuperAdminResponse200Item']]
    """

    kwargs = _get_kwargs(
        flag=flag,
        search=search,
        per_page=per_page,
        after_last_used_at=after_last_used_at,
        after_token_prefix=after_token_prefix,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    flag: Union[Unset, None, ListTokensAsSuperAdminFlag] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_last_used_at: Union[Unset, None, datetime.datetime] = UNSET,
    after_token_prefix: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListTokensAsSuperAdminResponse200Item"]]:
    """list every user's tokens, least recently used first (superadmin only, EE)

     Tokens the server expires or renews on its own are left out. Pages are read with a cursor: pass the
    last row's `last_used_at` and `token_prefix` to get the next page.

    Args:
        flag (Union[Unset, None, ListTokensAsSuperAdminFlag]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        after_last_used_at (Union[Unset, None, datetime.datetime]):
        after_token_prefix (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListTokensAsSuperAdminResponse200Item']
    """

    return sync_detailed(
        client=client,
        flag=flag,
        search=search,
        per_page=per_page,
        after_last_used_at=after_last_used_at,
        after_token_prefix=after_token_prefix,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    flag: Union[Unset, None, ListTokensAsSuperAdminFlag] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_last_used_at: Union[Unset, None, datetime.datetime] = UNSET,
    after_token_prefix: Union[Unset, None, str] = UNSET,
) -> Response[List["ListTokensAsSuperAdminResponse200Item"]]:
    """list every user's tokens, least recently used first (superadmin only, EE)

     Tokens the server expires or renews on its own are left out. Pages are read with a cursor: pass the
    last row's `last_used_at` and `token_prefix` to get the next page.

    Args:
        flag (Union[Unset, None, ListTokensAsSuperAdminFlag]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        after_last_used_at (Union[Unset, None, datetime.datetime]):
        after_token_prefix (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListTokensAsSuperAdminResponse200Item']]
    """

    kwargs = _get_kwargs(
        flag=flag,
        search=search,
        per_page=per_page,
        after_last_used_at=after_last_used_at,
        after_token_prefix=after_token_prefix,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    flag: Union[Unset, None, ListTokensAsSuperAdminFlag] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_last_used_at: Union[Unset, None, datetime.datetime] = UNSET,
    after_token_prefix: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListTokensAsSuperAdminResponse200Item"]]:
    """list every user's tokens, least recently used first (superadmin only, EE)

     Tokens the server expires or renews on its own are left out. Pages are read with a cursor: pass the
    last row's `last_used_at` and `token_prefix` to get the next page.

    Args:
        flag (Union[Unset, None, ListTokensAsSuperAdminFlag]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        after_last_used_at (Union[Unset, None, datetime.datetime]):
        after_token_prefix (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListTokensAsSuperAdminResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            flag=flag,
            search=search,
            per_page=per_page,
            after_last_used_at=after_last_used_at,
            after_token_prefix=after_token_prefix,
        )
    ).parsed
