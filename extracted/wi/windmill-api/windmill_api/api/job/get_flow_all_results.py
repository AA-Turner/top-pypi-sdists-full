from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_flow_all_results_response_200 import GetFlowAllResultsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    max_result_len: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["max_result_len"] = max_result_len

    params["step"] = step

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs_u/get_flow_all_results/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetFlowAllResultsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetFlowAllResultsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetFlowAllResultsResponse200]:
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
    max_result_len: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
) -> Response[GetFlowAllResultsResponse200]:
    """get statuses and truncated results for all jobs of a flow job's execution tree

    Args:
        workspace (str):
        id (str):
        max_result_len (Union[Unset, None, int]):
        step (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFlowAllResultsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        max_result_len=max_result_len,
        step=step,
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
    max_result_len: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
) -> Optional[GetFlowAllResultsResponse200]:
    """get statuses and truncated results for all jobs of a flow job's execution tree

    Args:
        workspace (str):
        id (str):
        max_result_len (Union[Unset, None, int]):
        step (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFlowAllResultsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        max_result_len=max_result_len,
        step=step,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_result_len: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
) -> Response[GetFlowAllResultsResponse200]:
    """get statuses and truncated results for all jobs of a flow job's execution tree

    Args:
        workspace (str):
        id (str):
        max_result_len (Union[Unset, None, int]):
        step (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFlowAllResultsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        max_result_len=max_result_len,
        step=step,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_result_len: Union[Unset, None, int] = UNSET,
    step: Union[Unset, None, str] = UNSET,
) -> Optional[GetFlowAllResultsResponse200]:
    """get statuses and truncated results for all jobs of a flow job's execution tree

    Args:
        workspace (str):
        id (str):
        max_result_len (Union[Unset, None, int]):
        step (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFlowAllResultsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            max_result_len=max_result_len,
            step=step,
        )
    ).parsed
