from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_addable_instance_users_response_200_item import ListAddableInstanceUsersResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["search"] = search

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/users/list_addable".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListAddableInstanceUsersResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAddableInstanceUsersResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListAddableInstanceUsersResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List["ListAddableInstanceUsersResponse200Item"]]:
    """list instance users that can still be added to this workspace (require to be super admin)

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAddableInstanceUsersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search=search,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List["ListAddableInstanceUsersResponse200Item"]]:
    """list instance users that can still be added to this workspace (require to be super admin)

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAddableInstanceUsersResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        search=search,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List["ListAddableInstanceUsersResponse200Item"]]:
    """list instance users that can still be added to this workspace (require to be super admin)

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAddableInstanceUsersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search=search,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List["ListAddableInstanceUsersResponse200Item"]]:
    """list instance users that can still be added to this workspace (require to be super admin)

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAddableInstanceUsersResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            search=search,
            per_page=per_page,
        )
    ).parsed
