from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_autoscaling_diagnostics_response_200 import GetAutoscalingDiagnosticsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    worker_group: str,
    *,
    include_decisions: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_decisions"] = include_decisions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/configs/autoscaling_diagnostics/{worker_group}".format(
            worker_group=worker_group,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetAutoscalingDiagnosticsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAutoscalingDiagnosticsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetAutoscalingDiagnosticsResponse200]:
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
    include_decisions: Union[Unset, None, bool] = UNSET,
) -> Response[GetAutoscalingDiagnosticsResponse200]:
    """Get the recorded autoscaling decisions of a worker group, and whether a recording is running

    Args:
        worker_group (str):
        include_decisions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAutoscalingDiagnosticsResponse200]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        include_decisions=include_decisions,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_decisions: Union[Unset, None, bool] = UNSET,
) -> Optional[GetAutoscalingDiagnosticsResponse200]:
    """Get the recorded autoscaling decisions of a worker group, and whether a recording is running

    Args:
        worker_group (str):
        include_decisions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAutoscalingDiagnosticsResponse200
    """

    return sync_detailed(
        worker_group=worker_group,
        client=client,
        include_decisions=include_decisions,
    ).parsed


async def asyncio_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_decisions: Union[Unset, None, bool] = UNSET,
) -> Response[GetAutoscalingDiagnosticsResponse200]:
    """Get the recorded autoscaling decisions of a worker group, and whether a recording is running

    Args:
        worker_group (str):
        include_decisions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAutoscalingDiagnosticsResponse200]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        include_decisions=include_decisions,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_decisions: Union[Unset, None, bool] = UNSET,
) -> Optional[GetAutoscalingDiagnosticsResponse200]:
    """Get the recorded autoscaling decisions of a worker group, and whether a recording is running

    Args:
        worker_group (str):
        include_decisions (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAutoscalingDiagnosticsResponse200
    """

    return (
        await asyncio_detailed(
            worker_group=worker_group,
            client=client,
            include_decisions=include_decisions,
        )
    ).parsed
