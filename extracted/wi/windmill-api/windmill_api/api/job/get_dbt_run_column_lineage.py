from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_dbt_run_column_lineage_response_200 import GetDbtRunColumnLineageResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    asset_path: List[str],
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_asset_path = asset_path

    params["asset_path"] = json_asset_path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/dbt_column_lineage/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetDbtRunColumnLineageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDbtRunColumnLineageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetDbtRunColumnLineageResponse200]:
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
    asset_path: List[str],
) -> Response[GetDbtRunColumnLineageResponse200]:
    """Get relations' project column lineage as one run saw it

     The same answer as `assets/column_lineage`, for the project version a single job ran — including the
    dbt editor's parse of its own buffer, whose graph belongs to that job and is reachable no other way.
    One project answers here, the one the run is of, since the graph this annotates is that project's
    too. Authorized through the job, the same gate as `dbt_graph`. Reaching the run is not on its own
    enough to read the project: a caller with no access to the script gets its relations and `ref()`
    edges from `dbt_graph` and an empty answer here, exactly as that endpoint redacts the model's SQL.

    Args:
        workspace (str):
        id (str):
        asset_path (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtRunColumnLineageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        asset_path=asset_path,
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
    asset_path: List[str],
) -> Optional[GetDbtRunColumnLineageResponse200]:
    """Get relations' project column lineage as one run saw it

     The same answer as `assets/column_lineage`, for the project version a single job ran — including the
    dbt editor's parse of its own buffer, whose graph belongs to that job and is reachable no other way.
    One project answers here, the one the run is of, since the graph this annotates is that project's
    too. Authorized through the job, the same gate as `dbt_graph`. Reaching the run is not on its own
    enough to read the project: a caller with no access to the script gets its relations and `ref()`
    edges from `dbt_graph` and an empty answer here, exactly as that endpoint redacts the model's SQL.

    Args:
        workspace (str):
        id (str):
        asset_path (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtRunColumnLineageResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        asset_path=asset_path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
) -> Response[GetDbtRunColumnLineageResponse200]:
    """Get relations' project column lineage as one run saw it

     The same answer as `assets/column_lineage`, for the project version a single job ran — including the
    dbt editor's parse of its own buffer, whose graph belongs to that job and is reachable no other way.
    One project answers here, the one the run is of, since the graph this annotates is that project's
    too. Authorized through the job, the same gate as `dbt_graph`. Reaching the run is not on its own
    enough to read the project: a caller with no access to the script gets its relations and `ref()`
    edges from `dbt_graph` and an empty answer here, exactly as that endpoint redacts the model's SQL.

    Args:
        workspace (str):
        id (str):
        asset_path (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDbtRunColumnLineageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        asset_path=asset_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_path: List[str],
) -> Optional[GetDbtRunColumnLineageResponse200]:
    """Get relations' project column lineage as one run saw it

     The same answer as `assets/column_lineage`, for the project version a single job ran — including the
    dbt editor's parse of its own buffer, whose graph belongs to that job and is reachable no other way.
    One project answers here, the one the run is of, since the graph this annotates is that project's
    too. Authorized through the job, the same gate as `dbt_graph`. Reaching the run is not on its own
    enough to read the project: a caller with no access to the script gets its relations and `ref()`
    edges from `dbt_graph` and an empty answer here, exactly as that endpoint redacts the model's SQL.

    Args:
        workspace (str):
        id (str):
        asset_path (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDbtRunColumnLineageResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            asset_path=asset_path,
        )
    ).parsed
