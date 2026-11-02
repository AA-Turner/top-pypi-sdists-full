from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    worker_group: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/settings/restart_worker_group/{worker_group}".format(
            worker_group=worker_group,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """restart worker group

     Send a restart signal to all workers in the specified worker group. Workers will gracefully shut
    down and are expected to be restarted by their supervisor. Requires devops role.

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """restart worker group

     Send a restart signal to all workers in the specified worker group. Workers will gracefully shut
    down and are expected to be restarted by their supervisor. Requires devops role.

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
