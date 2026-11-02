from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.recent_scorers_kind import RecentScorersKind
from ...models.recent_scorers_response_200_item import RecentScorersResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    kind: Union[Unset, None, RecentScorersKind] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_kind: Union[Unset, None, str] = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value if kind else None

    params["kind"] = json_kind

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai_evals/scorers/recent".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["RecentScorersResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RecentScorersResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["RecentScorersResponse200Item"]]:
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
    kind: Union[Unset, None, RecentScorersKind] = UNSET,
) -> Response[List["RecentScorersResponse200Item"]]:
    """list the scorers already in use in this workspace, most recent first

     Filtered twice, both times by what the caller can read: the datasets they come from, and the
    runnables themselves. A scorer they could not run does not appear.

    Args:
        workspace (str):
        kind (Union[Unset, None, RecentScorersKind]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['RecentScorersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, None, RecentScorersKind] = UNSET,
) -> Optional[List["RecentScorersResponse200Item"]]:
    """list the scorers already in use in this workspace, most recent first

     Filtered twice, both times by what the caller can read: the datasets they come from, and the
    runnables themselves. A scorer they could not run does not appear.

    Args:
        workspace (str):
        kind (Union[Unset, None, RecentScorersKind]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['RecentScorersResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        kind=kind,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, None, RecentScorersKind] = UNSET,
) -> Response[List["RecentScorersResponse200Item"]]:
    """list the scorers already in use in this workspace, most recent first

     Filtered twice, both times by what the caller can read: the datasets they come from, and the
    runnables themselves. A scorer they could not run does not appear.

    Args:
        workspace (str):
        kind (Union[Unset, None, RecentScorersKind]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['RecentScorersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, None, RecentScorersKind] = UNSET,
) -> Optional[List["RecentScorersResponse200Item"]]:
    """list the scorers already in use in this workspace, most recent first

     Filtered twice, both times by what the caller can read: the datasets they come from, and the
    runnables themselves. A scorer they could not run does not appear.

    Args:
        workspace (str):
        kind (Union[Unset, None, RecentScorersKind]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['RecentScorersResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            kind=kind,
        )
    ).parsed
