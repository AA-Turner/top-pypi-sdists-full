from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.list_schemas_order_type_0_item import ListSchemasOrderType0Item
from ...models.list_schemas_response_200 import ListSchemasResponse200
from ...models.list_schemas_sort_type_0_item import ListSchemasSortType0Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    pipeline_name: list[str] | None | Unset = UNSET,
    dataset_name: list[str] | None | Unset = UNSET,
    sort: list[ListSchemasSortType0Item] | None | Unset = UNSET,
    order: list[ListSchemasOrderType0Item] | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_pipeline_name: list[str] | None | Unset
    if isinstance(pipeline_name, Unset):
        json_pipeline_name = UNSET
    elif isinstance(pipeline_name, list):
        json_pipeline_name = pipeline_name

    else:
        json_pipeline_name = pipeline_name
    params["pipeline_name"] = json_pipeline_name

    json_dataset_name: list[str] | None | Unset
    if isinstance(dataset_name, Unset):
        json_dataset_name = UNSET
    elif isinstance(dataset_name, list):
        json_dataset_name = dataset_name

    else:
        json_dataset_name = dataset_name
    params["dataset_name"] = json_dataset_name

    json_sort: list[str] | None | Unset
    if isinstance(sort, Unset):
        json_sort = UNSET
    elif isinstance(sort, list):
        json_sort = []
        for sort_type_0_item_data in sort:
            sort_type_0_item = sort_type_0_item_data.value
            json_sort.append(sort_type_0_item)

    else:
        json_sort = sort
    params["sort"] = json_sort

    json_order: list[str] | None | Unset
    if isinstance(order, Unset):
        json_order = UNSET
    elif isinstance(order, list):
        json_order = []
        for order_type_0_item_data in order:
            order_type_0_item = order_type_0_item_data.value
            json_order.append(order_type_0_item)

    else:
        json_order = order
    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/schemas".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | ListSchemasResponse200 | None:
    if response.status_code == 200:
        response_200 = ListSchemasResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | ListSchemasResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    pipeline_name: list[str] | None | Unset = UNSET,
    dataset_name: list[str] | None | Unset = UNSET,
    sort: list[ListSchemasSortType0Item] | None | Unset = UNSET,
    order: list[ListSchemasOrderType0Item] | None | Unset = UNSET,
) -> Response[ErrorResponse400 | ListSchemasResponse200]:
    """ListSchemas

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        dataset_name (list[str] | None | Unset): Exact match on `dataset_name`. Repeat the
            parameter to match any of several values.
        sort (list[ListSchemasSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListSchemasOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ListSchemasResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        sort=sort,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    pipeline_name: list[str] | None | Unset = UNSET,
    dataset_name: list[str] | None | Unset = UNSET,
    sort: list[ListSchemasSortType0Item] | None | Unset = UNSET,
    order: list[ListSchemasOrderType0Item] | None | Unset = UNSET,
) -> ErrorResponse400 | ListSchemasResponse200 | None:
    """ListSchemas

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        dataset_name (list[str] | None | Unset): Exact match on `dataset_name`. Repeat the
            parameter to match any of several values.
        sort (list[ListSchemasSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListSchemasOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ListSchemasResponse200
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        limit=limit,
        offset=offset,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    pipeline_name: list[str] | None | Unset = UNSET,
    dataset_name: list[str] | None | Unset = UNSET,
    sort: list[ListSchemasSortType0Item] | None | Unset = UNSET,
    order: list[ListSchemasOrderType0Item] | None | Unset = UNSET,
) -> Response[ErrorResponse400 | ListSchemasResponse200]:
    """ListSchemas

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        dataset_name (list[str] | None | Unset): Exact match on `dataset_name`. Repeat the
            parameter to match any of several values.
        sort (list[ListSchemasSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListSchemasOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ListSchemasResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    pipeline_name: list[str] | None | Unset = UNSET,
    dataset_name: list[str] | None | Unset = UNSET,
    sort: list[ListSchemasSortType0Item] | None | Unset = UNSET,
    order: list[ListSchemasOrderType0Item] | None | Unset = UNSET,
) -> ErrorResponse400 | ListSchemasResponse200 | None:
    """ListSchemas

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        dataset_name (list[str] | None | Unset): Exact match on `dataset_name`. Repeat the
            parameter to match any of several values.
        sort (list[ListSchemasSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListSchemasOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ListSchemasResponse200
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            limit=limit,
            offset=offset,
            pipeline_name=pipeline_name,
            dataset_name=dataset_name,
            sort=sort,
            order=order,
        )
    ).parsed
