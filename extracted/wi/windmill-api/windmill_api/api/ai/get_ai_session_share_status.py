from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_ai_session_share_status_response_200 import GetAiSessionShareStatusResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    session_id: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["session_id"] = session_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai/shared_sessions/status".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetAiSessionShareStatusResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAiSessionShareStatusResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetAiSessionShareStatusResponse200]:
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
    session_id: str,
) -> Response[GetAiSessionShareStatusResponse200]:
    """get the calling user's share of one of their AI sessions

    Args:
        workspace (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAiSessionShareStatusResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        session_id=session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: str,
) -> Optional[GetAiSessionShareStatusResponse200]:
    """get the calling user's share of one of their AI sessions

    Args:
        workspace (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAiSessionShareStatusResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        session_id=session_id,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: str,
) -> Response[GetAiSessionShareStatusResponse200]:
    """get the calling user's share of one of their AI sessions

    Args:
        workspace (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAiSessionShareStatusResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        session_id=session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    session_id: str,
) -> Optional[GetAiSessionShareStatusResponse200]:
    """get the calling user's share of one of their AI sessions

    Args:
        workspace (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAiSessionShareStatusResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            session_id=session_id,
        )
    ).parsed
