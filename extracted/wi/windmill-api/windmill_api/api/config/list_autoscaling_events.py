from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_autoscaling_events_response_200_item import ListAutoscalingEventsResponse200Item
from ...types import Response


def _get_kwargs(
    worker_group: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/configs/list_autoscaling_events/{worker_group}".format(
            worker_group=worker_group,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListAutoscalingEventsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAutoscalingEventsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListAutoscalingEventsResponse200Item"]]:
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
) -> Response[List["ListAutoscalingEventsResponse200Item"]]:
    """List autoscaling events

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAutoscalingEventsResponse200Item']]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListAutoscalingEventsResponse200Item"]]:
    """List autoscaling events

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAutoscalingEventsResponse200Item']
    """

    return sync_detailed(
        worker_group=worker_group,
        client=client,
    ).parsed


async def asyncio_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["ListAutoscalingEventsResponse200Item"]]:
    """List autoscaling events

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAutoscalingEventsResponse200Item']]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListAutoscalingEventsResponse200Item"]]:
    """List autoscaling events

    Args:
        worker_group (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAutoscalingEventsResponse200Item']
    """

    return (
        await asyncio_detailed(
            worker_group=worker_group,
            client=client,
        )
    ).parsed
