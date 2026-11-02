from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    id: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["id"] = id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/ai_evals/experiments/collect".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[int]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(int, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
    id: str,
) -> Response[int]:
    """record what a run produced, so it outlives the jobs that produced it

     Called by a run's own flow as its last step. The answers and scores a run produced live in its jobs,
    which have their own retention; this copies them onto the run's rows. Reading a run does the same,
    so this is what covers a run nobody opened.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
) -> Optional[int]:
    """record what a run produced, so it outlives the jobs that produced it

     Called by a run's own flow as its last step. The answers and scores a run produced live in its jobs,
    which have their own retention; this copies them onto the run's rows. Reading a run does the same,
    so this is what covers a run nobody opened.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        id=id,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
) -> Response[int]:
    """record what a run produced, so it outlives the jobs that produced it

     Called by a run's own flow as its last step. The answers and scores a run produced live in its jobs,
    which have their own retention; this copies them onto the run's rows. Reading a run does the same,
    so this is what covers a run nobody opened.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
) -> Optional[int]:
    """record what a run produced, so it outlives the jobs that produced it

     Called by a run's own flow as its last step. The answers and scores a run produced live in its jobs,
    which have their own retention; this copies them onto the run's rows. Reading a run does the same,
    so this is what covers a run nobody opened.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            id=id,
        )
    ).parsed
