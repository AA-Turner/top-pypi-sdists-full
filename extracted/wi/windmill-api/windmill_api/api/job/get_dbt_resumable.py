from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/dbt_resumable/{id}".format(
            workspace=workspace,
            id=id,
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[str]]:
    """Whether a dbt retry by this caller would resume this run

     One failed run is saved per script per execution principal, so a `retry` resumes that one — not
    necessarily the run being looked at. Answers about THIS run alone: its own id when a retry submitted
    by this caller would resume it, null otherwise (a later run holds the state, the run left nothing to
    rebuild, or the caller's runs execute as another principal). Authorized through the job, like
    `run_progress`.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[str]]
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[str]]:
    """Whether a dbt retry by this caller would resume this run

     One failed run is saved per script per execution principal, so a `retry` resumes that one — not
    necessarily the run being looked at. Answers about THIS run alone: its own id when a retry submitted
    by this caller would resume it, null otherwise (a later run holds the state, the run left nothing to
    rebuild, or the caller's runs execute as another principal). Authorized through the job, like
    `run_progress`.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[str]
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[str]]:
    """Whether a dbt retry by this caller would resume this run

     One failed run is saved per script per execution principal, so a `retry` resumes that one — not
    necessarily the run being looked at. Answers about THIS run alone: its own id when a retry submitted
    by this caller would resume it, null otherwise (a later run holds the state, the run left nothing to
    rebuild, or the caller's runs execute as another principal). Authorized through the job, like
    `run_progress`.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[str]]:
    """Whether a dbt retry by this caller would resume this run

     One failed run is saved per script per execution principal, so a `retry` resumes that one — not
    necessarily the run being looked at. Answers about THIS run alone: its own id when a retry submitted
    by this caller would resume it, null otherwise (a later run holds the state, the run left nothing to
    rebuild, or the caller's runs execute as another principal). Authorized through the job, like
    `run_progress`.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
        )
    ).parsed
