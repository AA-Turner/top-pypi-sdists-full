from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_run_progress_response_200_item import GetRunProgressResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/run_progress/{id}".format(
            workspace=workspace,
            id=id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["GetRunProgressResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetRunProgressResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["GetRunProgressResponse200Item"]]:
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
) -> Response[List["GetRunProgressResponse200Item"]]:
    """List the per-relation progress one job has recorded so far

     Live materialization state for the relations a single job writes, keyed by relation. Polled while a
    run is in flight so a graph can move a node as its model completes. Authorized through the job, so a
    caller who may not read it is refused rather than told the run has no progress. An empty list means
    the job exists and has recorded nothing yet, or is unknown to this workspace.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetRunProgressResponse200Item']]
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
) -> Optional[List["GetRunProgressResponse200Item"]]:
    """List the per-relation progress one job has recorded so far

     Live materialization state for the relations a single job writes, keyed by relation. Polled while a
    run is in flight so a graph can move a node as its model completes. Authorized through the job, so a
    caller who may not read it is refused rather than told the run has no progress. An empty list means
    the job exists and has recorded nothing yet, or is unknown to this workspace.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetRunProgressResponse200Item']
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
) -> Response[List["GetRunProgressResponse200Item"]]:
    """List the per-relation progress one job has recorded so far

     Live materialization state for the relations a single job writes, keyed by relation. Polled while a
    run is in flight so a graph can move a node as its model completes. Authorized through the job, so a
    caller who may not read it is refused rather than told the run has no progress. An empty list means
    the job exists and has recorded nothing yet, or is unknown to this workspace.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetRunProgressResponse200Item']]
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
) -> Optional[List["GetRunProgressResponse200Item"]]:
    """List the per-relation progress one job has recorded so far

     Live materialization state for the relations a single job writes, keyed by relation. Polled while a
    run is in flight so a graph can move a node as its model completes. Authorized through the job, so a
    caller who may not read it is refused rather than told the run has no progress. An empty list means
    the job exists and has recorded nothing yet, or is unknown to this workspace.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetRunProgressResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
        )
    ).parsed
