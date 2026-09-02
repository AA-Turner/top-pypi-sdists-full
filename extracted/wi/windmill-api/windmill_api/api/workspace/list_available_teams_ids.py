from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_available_teams_ids_response_200 import ListAvailableTeamsIdsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    search: Union[Unset, None, str] = UNSET,
    next_link: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["search"] = search

    params["next_link"] = next_link

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/available_teams_ids".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAvailableTeamsIdsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAvailableTeamsIdsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAvailableTeamsIdsResponse200]:
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
    next_link: Union[Unset, None, str] = UNSET,
) -> Response[ListAvailableTeamsIdsResponse200]:
    """list available teams ids

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        next_link (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAvailableTeamsIdsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search=search,
        next_link=next_link,
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
    next_link: Union[Unset, None, str] = UNSET,
) -> Optional[ListAvailableTeamsIdsResponse200]:
    """list available teams ids

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        next_link (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAvailableTeamsIdsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        search=search,
        next_link=next_link,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    next_link: Union[Unset, None, str] = UNSET,
) -> Response[ListAvailableTeamsIdsResponse200]:
    """list available teams ids

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        next_link (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAvailableTeamsIdsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search=search,
        next_link=next_link,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, None, str] = UNSET,
    next_link: Union[Unset, None, str] = UNSET,
) -> Optional[ListAvailableTeamsIdsResponse200]:
    """list available teams ids

    Args:
        workspace (str):
        search (Union[Unset, None, str]):
        next_link (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAvailableTeamsIdsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            search=search,
            next_link=next_link,
        )
    ).parsed
