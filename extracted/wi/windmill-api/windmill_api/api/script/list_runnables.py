from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_runnables_order_by import ListRunnablesOrderBy
from ...models.list_runnables_response_200 import ListRunnablesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    order_by: Union[Unset, None, ListRunnablesOrderBy] = UNSET,
    order_desc: Union[Unset, None, bool] = UNSET,
    kinds: Union[Unset, None, str] = UNSET,
    show_archived: Union[Unset, None, bool] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    path_start: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_order_by: Union[Unset, None, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value if order_by else None

    params["order_by"] = json_order_by

    params["order_desc"] = order_desc

    params["kinds"] = kinds

    params["show_archived"] = show_archived

    params["include_without_main"] = include_without_main

    params["path_start"] = path_start

    params["label"] = label

    params["search"] = search

    params["per_page"] = per_page

    params["cursor"] = cursor

    params["include_draft_only"] = include_draft_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/runnables/list".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListRunnablesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListRunnablesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListRunnablesResponse200]:
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
    order_by: Union[Unset, None, ListRunnablesOrderBy] = UNSET,
    order_desc: Union[Unset, None, bool] = UNSET,
    kinds: Union[Unset, None, str] = UNSET,
    show_archived: Union[Unset, None, bool] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    path_start: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Response[ListRunnablesResponse200]:
    """list runnables (scripts, flows, apps) merged, ordered and keyset-paginated

    Args:
        workspace (str):
        order_by (Union[Unset, None, ListRunnablesOrderBy]):
        order_desc (Union[Unset, None, bool]):
        kinds (Union[Unset, None, str]):
        show_archived (Union[Unset, None, bool]):
        include_without_main (Union[Unset, None, bool]):
        path_start (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor (Union[Unset, None, str]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunnablesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        order_by=order_by,
        order_desc=order_desc,
        kinds=kinds,
        show_archived=show_archived,
        include_without_main=include_without_main,
        path_start=path_start,
        label=label,
        search=search,
        per_page=per_page,
        cursor=cursor,
        include_draft_only=include_draft_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, None, ListRunnablesOrderBy] = UNSET,
    order_desc: Union[Unset, None, bool] = UNSET,
    kinds: Union[Unset, None, str] = UNSET,
    show_archived: Union[Unset, None, bool] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    path_start: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Optional[ListRunnablesResponse200]:
    """list runnables (scripts, flows, apps) merged, ordered and keyset-paginated

    Args:
        workspace (str):
        order_by (Union[Unset, None, ListRunnablesOrderBy]):
        order_desc (Union[Unset, None, bool]):
        kinds (Union[Unset, None, str]):
        show_archived (Union[Unset, None, bool]):
        include_without_main (Union[Unset, None, bool]):
        path_start (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor (Union[Unset, None, str]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunnablesResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        order_by=order_by,
        order_desc=order_desc,
        kinds=kinds,
        show_archived=show_archived,
        include_without_main=include_without_main,
        path_start=path_start,
        label=label,
        search=search,
        per_page=per_page,
        cursor=cursor,
        include_draft_only=include_draft_only,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, None, ListRunnablesOrderBy] = UNSET,
    order_desc: Union[Unset, None, bool] = UNSET,
    kinds: Union[Unset, None, str] = UNSET,
    show_archived: Union[Unset, None, bool] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    path_start: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Response[ListRunnablesResponse200]:
    """list runnables (scripts, flows, apps) merged, ordered and keyset-paginated

    Args:
        workspace (str):
        order_by (Union[Unset, None, ListRunnablesOrderBy]):
        order_desc (Union[Unset, None, bool]):
        kinds (Union[Unset, None, str]):
        show_archived (Union[Unset, None, bool]):
        include_without_main (Union[Unset, None, bool]):
        path_start (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor (Union[Unset, None, str]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunnablesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        order_by=order_by,
        order_desc=order_desc,
        kinds=kinds,
        show_archived=show_archived,
        include_without_main=include_without_main,
        path_start=path_start,
        label=label,
        search=search,
        per_page=per_page,
        cursor=cursor,
        include_draft_only=include_draft_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, None, ListRunnablesOrderBy] = UNSET,
    order_desc: Union[Unset, None, bool] = UNSET,
    kinds: Union[Unset, None, str] = UNSET,
    show_archived: Union[Unset, None, bool] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    path_start: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Optional[ListRunnablesResponse200]:
    """list runnables (scripts, flows, apps) merged, ordered and keyset-paginated

    Args:
        workspace (str):
        order_by (Union[Unset, None, ListRunnablesOrderBy]):
        order_desc (Union[Unset, None, bool]):
        kinds (Union[Unset, None, str]):
        show_archived (Union[Unset, None, bool]):
        include_without_main (Union[Unset, None, bool]):
        path_start (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        per_page (Union[Unset, None, int]):
        cursor (Union[Unset, None, str]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunnablesResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            order_by=order_by,
            order_desc=order_desc,
            kinds=kinds,
            show_archived=show_archived,
            include_without_main=include_without_main,
            path_start=path_start,
            label=label,
            search=search,
            per_page=per_page,
            cursor=cursor,
            include_draft_only=include_draft_only,
        )
    ).parsed
