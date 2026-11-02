from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_queue_metrics_series_response_200 import GetQueueMetricsSeriesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    window_secs: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["window_secs"] = window_secs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/workers/queue_metrics_series",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetQueueMetricsSeriesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetQueueMetricsSeriesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetQueueMetricsSeriesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
) -> Response[GetQueueMetricsSeriesResponse200]:
    """get the queue metrics of a time window, as a bounded line per tag

    Args:
        window_secs (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueueMetricsSeriesResponse200]
    """

    kwargs = _get_kwargs(
        window_secs=window_secs,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
) -> Optional[GetQueueMetricsSeriesResponse200]:
    """get the queue metrics of a time window, as a bounded line per tag

    Args:
        window_secs (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueueMetricsSeriesResponse200
    """

    return sync_detailed(
        client=client,
        window_secs=window_secs,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
) -> Response[GetQueueMetricsSeriesResponse200]:
    """get the queue metrics of a time window, as a bounded line per tag

    Args:
        window_secs (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueueMetricsSeriesResponse200]
    """

    kwargs = _get_kwargs(
        window_secs=window_secs,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
) -> Optional[GetQueueMetricsSeriesResponse200]:
    """get the queue metrics of a time window, as a bounded line per tag

    Args:
        window_secs (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueueMetricsSeriesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            window_secs=window_secs,
        )
    ).parsed
