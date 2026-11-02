from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.cloud_agent_computer_session import CloudAgentComputerSession
from ...models.error_envelope import ErrorEnvelope
from ...types import Response


def _get_kwargs(
    agent_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/agents/{agent_id}/computer-sessions".format(
            agent_id=quote(str(agent_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CloudAgentComputerSession | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = CloudAgentComputerSession.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ErrorEnvelope.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ErrorEnvelope.from_dict(response.json())

        return response_504

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CloudAgentComputerSession | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CloudAgentComputerSession | ErrorEnvelope]:
    """Open a short-lived Cloud Agent computer session

     Enables the Agent runtime's VNC desktop if needed, waits for it to become ready, and returns a
    short-lived Runta browser session. Long-lived API credentials remain outside the renderer; clients
    pass the returned protocols only to the VNC WebSocket handshake.

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloudAgentComputerSession | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> CloudAgentComputerSession | ErrorEnvelope | None:
    """Open a short-lived Cloud Agent computer session

     Enables the Agent runtime's VNC desktop if needed, waits for it to become ready, and returns a
    short-lived Runta browser session. Long-lived API credentials remain outside the renderer; clients
    pass the returned protocols only to the VNC WebSocket handshake.

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloudAgentComputerSession | ErrorEnvelope
    """

    return sync_detailed(
        agent_id=agent_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CloudAgentComputerSession | ErrorEnvelope]:
    """Open a short-lived Cloud Agent computer session

     Enables the Agent runtime's VNC desktop if needed, waits for it to become ready, and returns a
    short-lived Runta browser session. Long-lived API credentials remain outside the renderer; clients
    pass the returned protocols only to the VNC WebSocket handshake.

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloudAgentComputerSession | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
) -> CloudAgentComputerSession | ErrorEnvelope | None:
    """Open a short-lived Cloud Agent computer session

     Enables the Agent runtime's VNC desktop if needed, waits for it to become ready, and returns a
    short-lived Runta browser session. Long-lived API credentials remain outside the renderer; clients
    pass the returned protocols only to the VNC WebSocket handshake.

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloudAgentComputerSession | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            agent_id=agent_id,
            client=client,
        )
    ).parsed
