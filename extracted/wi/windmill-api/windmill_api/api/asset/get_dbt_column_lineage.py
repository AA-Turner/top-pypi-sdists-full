from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_dbt_column_lineage_response_200 import GetDbtColumnLineageResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    asset_path: List[str],
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_asset_path = asset_path

    params["asset_path"] = json_asset_path

    params["dbt_script_hash"] = dbt_script_hash

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/assets/column_lineage".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetDbtColumnLineageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDbtColumnLineageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetDbtColumnLineageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Response[GetDbtColumnLineageResponse200]:
    """Column-level lineage of a set of dbt relations

     The direct (`copy` / `mod`) column-to-column lineage the given relations' columns sit in — the
    connected component around them, from the engine's static analysis. Not their own edges, which would
    stop one hop out since a column trace walks transitively, and not a whole project's, which carries
    model families the selection cannot reach.
    Several relations, answered as one union, because one selection reaches several: a script's output
    column can derive from columns of several dbt models. Unpinned, the component crosses projects — a
    relation one project produces is another's source — and the caller's access is decided again for
    every project it reaches, so a trace ends where their grants do. A pinned answer, by version here or
    by job on the run route, is one project's.
    Its own endpoint rather than a field on the asset graph: the graph is folder-wide and polled by a
    run page, while this is rendered for one selection at a time. Empty for projects that did not opt
    into the analysis pass (`column_lineage: true`), which is the ordinary case. The indirect `scan`
    kind is stored but never served: it reaches every output column of its model.

    Args:
        workspace (str):
        asset_path (List[str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtColumnLineageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        asset_path=asset_path,
        dbt_script_hash=dbt_script_hash,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbtColumnLineageResponse200]:
    """Column-level lineage of a set of dbt relations

     The direct (`copy` / `mod`) column-to-column lineage the given relations' columns sit in — the
    connected component around them, from the engine's static analysis. Not their own edges, which would
    stop one hop out since a column trace walks transitively, and not a whole project's, which carries
    model families the selection cannot reach.
    Several relations, answered as one union, because one selection reaches several: a script's output
    column can derive from columns of several dbt models. Unpinned, the component crosses projects — a
    relation one project produces is another's source — and the caller's access is decided again for
    every project it reaches, so a trace ends where their grants do. A pinned answer, by version here or
    by job on the run route, is one project's.
    Its own endpoint rather than a field on the asset graph: the graph is folder-wide and polled by a
    run page, while this is rendered for one selection at a time. Empty for projects that did not opt
    into the analysis pass (`column_lineage: true`), which is the ordinary case. The indirect `scan`
    kind is stored but never served: it reaches every output column of its model.

    Args:
        workspace (str):
        asset_path (List[str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtColumnLineageResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        asset_path=asset_path,
        dbt_script_hash=dbt_script_hash,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Response[GetDbtColumnLineageResponse200]:
    """Column-level lineage of a set of dbt relations

     The direct (`copy` / `mod`) column-to-column lineage the given relations' columns sit in — the
    connected component around them, from the engine's static analysis. Not their own edges, which would
    stop one hop out since a column trace walks transitively, and not a whole project's, which carries
    model families the selection cannot reach.
    Several relations, answered as one union, because one selection reaches several: a script's output
    column can derive from columns of several dbt models. Unpinned, the component crosses projects — a
    relation one project produces is another's source — and the caller's access is decided again for
    every project it reaches, so a trace ends where their grants do. A pinned answer, by version here or
    by job on the run route, is one project's.
    Its own endpoint rather than a field on the asset graph: the graph is folder-wide and polled by a
    run page, while this is rendered for one selection at a time. Empty for projects that did not opt
    into the analysis pass (`column_lineage: true`), which is the ordinary case. The indirect `scan`
    kind is stored but never served: it reaches every output column of its model.

    Args:
        workspace (str):
        asset_path (List[str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtColumnLineageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        asset_path=asset_path,
        dbt_script_hash=dbt_script_hash,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
    dbt_script_hash: Union[Unset, None, str] = UNSET,
) -> Optional[GetDbtColumnLineageResponse200]:
    """Column-level lineage of a set of dbt relations

     The direct (`copy` / `mod`) column-to-column lineage the given relations' columns sit in — the
    connected component around them, from the engine's static analysis. Not their own edges, which would
    stop one hop out since a column trace walks transitively, and not a whole project's, which carries
    model families the selection cannot reach.
    Several relations, answered as one union, because one selection reaches several: a script's output
    column can derive from columns of several dbt models. Unpinned, the component crosses projects — a
    relation one project produces is another's source — and the caller's access is decided again for
    every project it reaches, so a trace ends where their grants do. A pinned answer, by version here or
    by job on the run route, is one project's.
    Its own endpoint rather than a field on the asset graph: the graph is folder-wide and polled by a
    run page, while this is rendered for one selection at a time. Empty for projects that did not opt
    into the analysis pass (`column_lineage: true`), which is the ordinary case. The indirect `scan`
    kind is stored but never served: it reaches every output column of its model.

    Args:
        workspace (str):
        asset_path (List[str]):
        dbt_script_hash (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtColumnLineageResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            asset_path=asset_path,
            dbt_script_hash=dbt_script_hash,
        )
    ).parsed
