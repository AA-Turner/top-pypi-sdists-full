from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.experiment_results_response_200 import ExperimentResultsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    id: str,
    baseline: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["id"] = id

    params["baseline"] = baseline

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai_evals/experiments/results/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExperimentResultsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExperimentResultsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExperimentResultsResponse200]:
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
    id: str,
    baseline: Union[Unset, None, str] = UNSET,
) -> Response[ExperimentResultsResponse200]:
    """read an experiment's results, one row per case

    Args:
        workspace (str):
        path (str):
        id (str):
        baseline (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExperimentResultsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        id=id,
        baseline=baseline,
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
    id: str,
    baseline: Union[Unset, None, str] = UNSET,
) -> Optional[ExperimentResultsResponse200]:
    """read an experiment's results, one row per case

    Args:
        workspace (str):
        path (str):
        id (str):
        baseline (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExperimentResultsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
        id=id,
        baseline=baseline,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    baseline: Union[Unset, None, str] = UNSET,
) -> Response[ExperimentResultsResponse200]:
    """read an experiment's results, one row per case

    Args:
        workspace (str):
        path (str):
        id (str):
        baseline (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExperimentResultsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        id=id,
        baseline=baseline,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    baseline: Union[Unset, None, str] = UNSET,
) -> Optional[ExperimentResultsResponse200]:
    """read an experiment's results, one row per case

    Args:
        workspace (str):
        path (str):
        id (str):
        baseline (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExperimentResultsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
            id=id,
            baseline=baseline,
        )
    ).parsed
