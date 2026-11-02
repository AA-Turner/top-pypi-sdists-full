from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_queue_position_response_200 import GetQueuePositionResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    scheduled_for: int,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/queue/position/{scheduled_for}".format(
            workspace=workspace,
            scheduled_for=scheduled_for,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetQueuePositionResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetQueuePositionResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetQueuePositionResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    scheduled_for: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetQueuePositionResponse200]:
    """get queue position for a job

    Args:
        workspace (str):
        scheduled_for (int): The scheduled for timestamp in milliseconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueuePositionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        scheduled_for=scheduled_for,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    scheduled_for: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetQueuePositionResponse200]:
    """get queue position for a job

    Args:
        workspace (str):
        scheduled_for (int): The scheduled for timestamp in milliseconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueuePositionResponse200
    """

    return sync_detailed(
        workspace=workspace,
        scheduled_for=scheduled_for,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    scheduled_for: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetQueuePositionResponse200]:
    """get queue position for a job

    Args:
        workspace (str):
        scheduled_for (int): The scheduled for timestamp in milliseconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueuePositionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        scheduled_for=scheduled_for,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    scheduled_for: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetQueuePositionResponse200]:
    """get queue position for a job

    Args:
        workspace (str):
        scheduled_for (int): The scheduled for timestamp in milliseconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueuePositionResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            scheduled_for=scheduled_for,
            client=client,
        )
    ).parsed
