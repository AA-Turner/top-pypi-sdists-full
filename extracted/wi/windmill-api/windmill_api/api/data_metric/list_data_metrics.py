from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_data_metrics_response_200 import ListDataMetricsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    table: Union[Unset, None, str] = UNSET,
    path_prefix: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor_table: Union[Unset, None, str] = UNSET,
    cursor_kind: Union[Unset, None, str] = UNSET,
    cursor_name: Union[Unset, None, str] = UNSET,
    cursor_script: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["table"] = table

    params["path_prefix"] = path_prefix

    params["per_page"] = per_page

    params["cursor_table"] = cursor_table

    params["cursor_kind"] = cursor_kind

    params["cursor_name"] = cursor_name

    params["cursor_script"] = cursor_script

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/data_metrics/list".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListDataMetricsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListDataMetricsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListDataMetricsResponse200]:
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
    table: Union[Unset, None, str] = UNSET,
    path_prefix: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor_table: Union[Unset, None, str] = UNSET,
    cursor_kind: Union[Unset, None, str] = UNSET,
    cursor_name: Union[Unset, None, str] = UNSET,
    cursor_script: Union[Unset, None, str] = UNSET,
) -> Response[ListDataMetricsResponse200]:
    """list declared measures and dimensions on DuckLake tables

     Call this before writing any aggregate query over a DuckLake table. A declared measure is the
    canonical definition of that number, and reproducing it yourself will silently disagree with it (a
    `revenue` measure typically excludes refunds or test rows). Filter by `table` for one table's
    declarations, or by `path_prefix` (e.g. `f/analytics`) for everything declared under a folder; omit
    both to browse the whole catalog. Results are keyset-paged: a full page may mean more remain, so
    continue with the `cursor_*` params rather than assuming a measure does not exist. Use each returned
    `expr` verbatim, and when a measure has a `filter` write it as `expr FILTER (WHERE filter)` so
    measures with different predicates can share one GROUP BY. If a number you need has no declared
    measure, write your own aggregate as usual. Results are limited to declarations whose producing
    script the caller can read.

    Args:
        workspace (str):
        table (Union[Unset, None, str]):
        path_prefix (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor_table (Union[Unset, None, str]):
        cursor_kind (Union[Unset, None, str]):
        cursor_name (Union[Unset, None, str]):
        cursor_script (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDataMetricsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        table=table,
        path_prefix=path_prefix,
        per_page=per_page,
        cursor_table=cursor_table,
        cursor_kind=cursor_kind,
        cursor_name=cursor_name,
        cursor_script=cursor_script,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    table: Union[Unset, None, str] = UNSET,
    path_prefix: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor_table: Union[Unset, None, str] = UNSET,
    cursor_kind: Union[Unset, None, str] = UNSET,
    cursor_name: Union[Unset, None, str] = UNSET,
    cursor_script: Union[Unset, None, str] = UNSET,
) -> Optional[ListDataMetricsResponse200]:
    """list declared measures and dimensions on DuckLake tables

     Call this before writing any aggregate query over a DuckLake table. A declared measure is the
    canonical definition of that number, and reproducing it yourself will silently disagree with it (a
    `revenue` measure typically excludes refunds or test rows). Filter by `table` for one table's
    declarations, or by `path_prefix` (e.g. `f/analytics`) for everything declared under a folder; omit
    both to browse the whole catalog. Results are keyset-paged: a full page may mean more remain, so
    continue with the `cursor_*` params rather than assuming a measure does not exist. Use each returned
    `expr` verbatim, and when a measure has a `filter` write it as `expr FILTER (WHERE filter)` so
    measures with different predicates can share one GROUP BY. If a number you need has no declared
    measure, write your own aggregate as usual. Results are limited to declarations whose producing
    script the caller can read.

    Args:
        workspace (str):
        table (Union[Unset, None, str]):
        path_prefix (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor_table (Union[Unset, None, str]):
        cursor_kind (Union[Unset, None, str]):
        cursor_name (Union[Unset, None, str]):
        cursor_script (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDataMetricsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        table=table,
        path_prefix=path_prefix,
        per_page=per_page,
        cursor_table=cursor_table,
        cursor_kind=cursor_kind,
        cursor_name=cursor_name,
        cursor_script=cursor_script,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    table: Union[Unset, None, str] = UNSET,
    path_prefix: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor_table: Union[Unset, None, str] = UNSET,
    cursor_kind: Union[Unset, None, str] = UNSET,
    cursor_name: Union[Unset, None, str] = UNSET,
    cursor_script: Union[Unset, None, str] = UNSET,
) -> Response[ListDataMetricsResponse200]:
    """list declared measures and dimensions on DuckLake tables

     Call this before writing any aggregate query over a DuckLake table. A declared measure is the
    canonical definition of that number, and reproducing it yourself will silently disagree with it (a
    `revenue` measure typically excludes refunds or test rows). Filter by `table` for one table's
    declarations, or by `path_prefix` (e.g. `f/analytics`) for everything declared under a folder; omit
    both to browse the whole catalog. Results are keyset-paged: a full page may mean more remain, so
    continue with the `cursor_*` params rather than assuming a measure does not exist. Use each returned
    `expr` verbatim, and when a measure has a `filter` write it as `expr FILTER (WHERE filter)` so
    measures with different predicates can share one GROUP BY. If a number you need has no declared
    measure, write your own aggregate as usual. Results are limited to declarations whose producing
    script the caller can read.

    Args:
        workspace (str):
        table (Union[Unset, None, str]):
        path_prefix (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor_table (Union[Unset, None, str]):
        cursor_kind (Union[Unset, None, str]):
        cursor_name (Union[Unset, None, str]):
        cursor_script (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDataMetricsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        table=table,
        path_prefix=path_prefix,
        per_page=per_page,
        cursor_table=cursor_table,
        cursor_kind=cursor_kind,
        cursor_name=cursor_name,
        cursor_script=cursor_script,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    table: Union[Unset, None, str] = UNSET,
    path_prefix: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor_table: Union[Unset, None, str] = UNSET,
    cursor_kind: Union[Unset, None, str] = UNSET,
    cursor_name: Union[Unset, None, str] = UNSET,
    cursor_script: Union[Unset, None, str] = UNSET,
) -> Optional[ListDataMetricsResponse200]:
    """list declared measures and dimensions on DuckLake tables

     Call this before writing any aggregate query over a DuckLake table. A declared measure is the
    canonical definition of that number, and reproducing it yourself will silently disagree with it (a
    `revenue` measure typically excludes refunds or test rows). Filter by `table` for one table's
    declarations, or by `path_prefix` (e.g. `f/analytics`) for everything declared under a folder; omit
    both to browse the whole catalog. Results are keyset-paged: a full page may mean more remain, so
    continue with the `cursor_*` params rather than assuming a measure does not exist. Use each returned
    `expr` verbatim, and when a measure has a `filter` write it as `expr FILTER (WHERE filter)` so
    measures with different predicates can share one GROUP BY. If a number you need has no declared
    measure, write your own aggregate as usual. Results are limited to declarations whose producing
    script the caller can read.

    Args:
        workspace (str):
        table (Union[Unset, None, str]):
        path_prefix (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor_table (Union[Unset, None, str]):
        cursor_kind (Union[Unset, None, str]):
        cursor_name (Union[Unset, None, str]):
        cursor_script (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDataMetricsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            table=table,
            path_prefix=path_prefix,
            per_page=per_page,
            cursor_table=cursor_table,
            cursor_kind=cursor_kind,
            cursor_name=cursor_name,
            cursor_script=cursor_script,
        )
    ).parsed
