from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_dispatch_events_response_200_item import ListDispatchEventsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs_u/dispatch_events/{id}".format(
            workspace=workspace,
            id=id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListDispatchEventsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListDispatchEventsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListDispatchEventsResponse200Item"]]:
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
) -> Response[List["ListDispatchEventsResponse200Item"]]:
    """list asset-trigger dispatch events for a producer job

     Returns the chronological log of decisions the asset-trigger dispatcher made after this producer job
    completed. Each row is one (subscriber, asset write) decision: `dispatched` (with `child_job_id`),
    `join_pending` (with `received_inputs` / `required_inputs` / `partition`), or `skipped` (with
    `reason`). Rows are reaped automatically when the producer's `v2_job` row is deleted by the
    retention sweep.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListDispatchEventsResponse200Item']]
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
) -> Optional[List["ListDispatchEventsResponse200Item"]]:
    """list asset-trigger dispatch events for a producer job

     Returns the chronological log of decisions the asset-trigger dispatcher made after this producer job
    completed. Each row is one (subscriber, asset write) decision: `dispatched` (with `child_job_id`),
    `join_pending` (with `received_inputs` / `required_inputs` / `partition`), or `skipped` (with
    `reason`). Rows are reaped automatically when the producer's `v2_job` row is deleted by the
    retention sweep.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListDispatchEventsResponse200Item']
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
) -> Response[List["ListDispatchEventsResponse200Item"]]:
    """list asset-trigger dispatch events for a producer job

     Returns the chronological log of decisions the asset-trigger dispatcher made after this producer job
    completed. Each row is one (subscriber, asset write) decision: `dispatched` (with `child_job_id`),
    `join_pending` (with `received_inputs` / `required_inputs` / `partition`), or `skipped` (with
    `reason`). Rows are reaped automatically when the producer's `v2_job` row is deleted by the
    retention sweep.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListDispatchEventsResponse200Item']]
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
) -> Optional[List["ListDispatchEventsResponse200Item"]]:
    """list asset-trigger dispatch events for a producer job

     Returns the chronological log of decisions the asset-trigger dispatcher made after this producer job
    completed. Each row is one (subscriber, asset write) decision: `dispatched` (with `child_job_id`),
    `join_pending` (with `received_inputs` / `required_inputs` / `partition`), or `skipped` (with
    `reason`). Rows are reaped automatically when the producer's `v2_job` row is deleted by the
    retention sweep.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListDispatchEventsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
        )
    ).parsed
