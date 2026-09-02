from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_log_cleanup_status_response_200 import GetLogCleanupStatusResponse200
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/settings/log_cleanup_status",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Optional[GetLogCleanupStatusResponse200]]:
    if response.status_code == HTTPStatus.OK:
        _response_200 = response.json()
        response_200: Optional[GetLogCleanupStatusResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = GetLogCleanupStatusResponse200.from_dict(_response_200)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Optional[GetLogCleanupStatusResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetLogCleanupStatusResponse200]]:
    """get status of the manual log cleanup task

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetLogCleanupStatusResponse200]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetLogCleanupStatusResponse200]]:
    """get status of the manual log cleanup task

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetLogCleanupStatusResponse200]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetLogCleanupStatusResponse200]]:
    """get status of the manual log cleanup task

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetLogCleanupStatusResponse200]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetLogCleanupStatusResponse200]]:
    """get status of the manual log cleanup task

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetLogCleanupStatusResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
