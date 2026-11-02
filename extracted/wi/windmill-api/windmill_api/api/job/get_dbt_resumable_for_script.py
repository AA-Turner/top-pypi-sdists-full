from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/dbt_resumable_script/p/{path}".format(
            workspace=workspace,
            path=path,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Optional[str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Optional[str], response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Optional[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[str]]:
    """Which run a dbt retry of this script would resume for the caller

     A `retry` requires `dbt_retry_job`, and the run form has no job id to hand. Returns the one the
    caller's own retry would land on — the saved failure for the principal the run would execute as,
    which is the script's author for an `on_behalf_of` script and the caller otherwise — and only when
    that run is one the caller may read. Null when there is nothing to resume, or nothing this caller
    may be told about.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[str]]:
    """Which run a dbt retry of this script would resume for the caller

     A `retry` requires `dbt_retry_job`, and the run form has no job id to hand. Returns the one the
    caller's own retry would land on — the saved failure for the principal the run would execute as,
    which is the script's author for an `on_behalf_of` script and the caller otherwise — and only when
    that run is one the caller may read. Null when there is nothing to resume, or nothing this caller
    may be told about.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[str]
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[str]]:
    """Which run a dbt retry of this script would resume for the caller

     A `retry` requires `dbt_retry_job`, and the run form has no job id to hand. Returns the one the
    caller's own retry would land on — the saved failure for the principal the run would execute as,
    which is the script's author for an `on_behalf_of` script and the caller otherwise — and only when
    that run is one the caller may read. Null when there is nothing to resume, or nothing this caller
    may be told about.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[str]]:
    """Which run a dbt retry of this script would resume for the caller

     A `retry` requires `dbt_retry_job`, and the run form has no job id to hand. Returns the one the
    caller's own retry would land on — the saved failure for the principal the run would execute as,
    which is the script's author for an `on_behalf_of` script and the caller otherwise — and only when
    that run is one the caller may read. Null when there is nothing to resume, or nothing this caller
    may be told about.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
        )
    ).parsed
