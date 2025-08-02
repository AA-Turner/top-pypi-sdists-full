from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_blacklisted_agent_tokens_response_200_item import ListBlacklistedAgentTokensResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_expired: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_expired"] = include_expired

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/agent_workers/list_blacklisted_tokens",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListBlacklistedAgentTokensResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListBlacklistedAgentTokensResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListBlacklistedAgentTokensResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_expired: Union[Unset, None, bool] = False,
) -> Response[List["ListBlacklistedAgentTokensResponse200Item"]]:
    """list blacklisted agent tokens (requires super admin)

    Args:
        include_expired (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListBlacklistedAgentTokensResponse200Item']]
    """

    kwargs = _get_kwargs(
        include_expired=include_expired,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    include_expired: Union[Unset, None, bool] = False,
) -> Optional[List["ListBlacklistedAgentTokensResponse200Item"]]:
    """list blacklisted agent tokens (requires super admin)

    Args:
        include_expired (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListBlacklistedAgentTokensResponse200Item']
    """

    return sync_detailed(
        client=client,
        include_expired=include_expired,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_expired: Union[Unset, None, bool] = False,
) -> Response[List["ListBlacklistedAgentTokensResponse200Item"]]:
    """list blacklisted agent tokens (requires super admin)

    Args:
        include_expired (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListBlacklistedAgentTokensResponse200Item']]
    """

    kwargs = _get_kwargs(
        include_expired=include_expired,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    include_expired: Union[Unset, None, bool] = False,
) -> Optional[List["ListBlacklistedAgentTokensResponse200Item"]]:
    """list blacklisted agent tokens (requires super admin)

    Args:
        include_expired (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListBlacklistedAgentTokensResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            include_expired=include_expired,
        )
    ).parsed
