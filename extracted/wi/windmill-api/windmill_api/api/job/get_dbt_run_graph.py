from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_dbt_run_graph_response_200 import GetDbtRunGraphResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["asset_kinds"] = asset_kinds

    params["folder"] = folder

    params["dbt_script_hash"] = dbt_script_hash

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/dbt_graph/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetDbtRunGraphResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDbtRunGraphResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetDbtRunGraphResponse200]:
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
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Response[GetDbtRunGraphResponse200]:
    """Get the asset graph as one run saw it

     The workspace asset graph with its dbt half pinned to what a single run built. Only a dynamic
    descriptor (a `{{ }}` placeholder in `vars`) leaves a per-run snapshot; without one for this job the
    pinned version's own graph answers, so a run page may use this route unconditionally. Authorized
    through the job, the same gate as `run_progress` — pinning to a run is job-scoped, which is why
    `assets/graph` cannot do it.

    Args:
        workspace (str):
        id (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtRunGraphResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        asset_kinds=asset_kinds,
        folder=folder,
        dbt_script_hash=dbt_script_hash,
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
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbtRunGraphResponse200]:
    """Get the asset graph as one run saw it

     The workspace asset graph with its dbt half pinned to what a single run built. Only a dynamic
    descriptor (a `{{ }}` placeholder in `vars`) leaves a per-run snapshot; without one for this job the
    pinned version's own graph answers, so a run page may use this route unconditionally. Authorized
    through the job, the same gate as `run_progress` — pinning to a run is job-scoped, which is why
    `assets/graph` cannot do it.

    Args:
        workspace (str):
        id (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtRunGraphResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        asset_kinds=asset_kinds,
        folder=folder,
        dbt_script_hash=dbt_script_hash,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Response[GetDbtRunGraphResponse200]:
    """Get the asset graph as one run saw it

     The workspace asset graph with its dbt half pinned to what a single run built. Only a dynamic
    descriptor (a `{{ }}` placeholder in `vars`) leaves a per-run snapshot; without one for this job the
    pinned version's own graph answers, so a run page may use this route unconditionally. Authorized
    through the job, the same gate as `run_progress` — pinning to a run is job-scoped, which is why
    `assets/graph` cannot do it.

    Args:
        workspace (str):
        id (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtRunGraphResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        asset_kinds=asset_kinds,
        folder=folder,
        dbt_script_hash=dbt_script_hash,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbtRunGraphResponse200]:
    """Get the asset graph as one run saw it

     The workspace asset graph with its dbt half pinned to what a single run built. Only a dynamic
    descriptor (a `{{ }}` placeholder in `vars`) leaves a per-run snapshot; without one for this job the
    pinned version's own graph answers, so a run page may use this route unconditionally. Authorized
    through the job, the same gate as `run_progress` — pinning to a run is job-scoped, which is why
    `assets/graph` cannot do it.

    Args:
        workspace (str):
        id (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtRunGraphResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            asset_kinds=asset_kinds,
            folder=folder,
            dbt_script_hash=dbt_script_hash,
        )
    ).parsed
