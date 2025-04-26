import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.list_workflow_flowcharts_sort import ListWorkflowFlowchartsSort
from ...models.not_found_error import NotFoundError
from ...models.workflow_flowchart_paginated_list import WorkflowFlowchartPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListWorkflowFlowchartsSort] = ListWorkflowFlowchartsSort.CREATEDATDESC,
    created_at: Union[Unset, datetime.date] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/workflow-flowcharts".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    json_created_at: Union[Unset, str] = UNSET
    if not isinstance(created_at, Unset):
        json_created_at = created_at.isoformat()

    params: Dict[str, Any] = {}
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(json_created_at, Unset) and json_created_at is not None:
        params["createdAt"] = json_created_at
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    if response.status_code == 200:
        response_200 = WorkflowFlowchartPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListWorkflowFlowchartsSort] = ListWorkflowFlowchartsSort.CREATEDATDESC,
    created_at: Union[Unset, datetime.date] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Response[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        sort=sort,
        created_at=created_at,
        next_token=next_token,
        page_size=page_size,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListWorkflowFlowchartsSort] = ListWorkflowFlowchartsSort.CREATEDATDESC,
    created_at: Union[Unset, datetime.date] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Optional[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    """ List workflow flowcharts """

    return sync_detailed(
        client=client,
        ids=ids,
        sort=sort,
        created_at=created_at,
        next_token=next_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListWorkflowFlowchartsSort] = ListWorkflowFlowchartsSort.CREATEDATDESC,
    created_at: Union[Unset, datetime.date] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Response[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        sort=sort,
        created_at=created_at,
        next_token=next_token,
        page_size=page_size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    ids: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListWorkflowFlowchartsSort] = ListWorkflowFlowchartsSort.CREATEDATDESC,
    created_at: Union[Unset, datetime.date] = UNSET,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
) -> Optional[Union[WorkflowFlowchartPaginatedList, NotFoundError]]:
    """ List workflow flowcharts """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
            sort=sort,
            created_at=created_at,
            next_token=next_token,
            page_size=page_size,
        )
    ).parsed
