from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_available_teams_channels_response_200 import ListAvailableTeamsChannelsResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    team_id: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["team_id"] = team_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/available_teams_channels".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAvailableTeamsChannelsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAvailableTeamsChannelsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAvailableTeamsChannelsResponse200]:
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
    team_id: str,
) -> Response[ListAvailableTeamsChannelsResponse200]:
    """list available channels for a specific team

    Args:
        workspace (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAvailableTeamsChannelsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        team_id=team_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: str,
) -> Optional[ListAvailableTeamsChannelsResponse200]:
    """list available channels for a specific team

    Args:
        workspace (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAvailableTeamsChannelsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        team_id=team_id,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: str,
) -> Response[ListAvailableTeamsChannelsResponse200]:
    """list available channels for a specific team

    Args:
        workspace (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAvailableTeamsChannelsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        team_id=team_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    team_id: str,
) -> Optional[ListAvailableTeamsChannelsResponse200]:
    """list available channels for a specific team

    Args:
        workspace (str):
        team_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAvailableTeamsChannelsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            team_id=team_id,
        )
    ).parsed
