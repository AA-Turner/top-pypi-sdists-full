from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_component_usage import CategoryComponentUsage
from ...models.category_component_usage_field_enum import CategoryComponentUsageFieldEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-category-component-usages/{id}/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CategoryComponentUsage:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CategoryComponentUsage.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CategoryComponentUsage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
) -> Response[CategoryComponentUsage]:
    """Retrieve an aggregated category component usage record

     Returns the details of a single aggregated usage record for a category component, identified by its
    database ID.

    Args:
        id (int):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryComponentUsage]
    """

    kwargs = _get_kwargs(
        id=id,
        field=field,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
) -> CategoryComponentUsage:
    """Retrieve an aggregated category component usage record

     Returns the details of a single aggregated usage record for a category component, identified by its
    database ID.

    Args:
        id (int):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryComponentUsage
    """

    return sync_detailed(
        id=id,
        client=client,
        field=field,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
) -> Response[CategoryComponentUsage]:
    """Retrieve an aggregated category component usage record

     Returns the details of a single aggregated usage record for a category component, identified by its
    database ID.

    Args:
        id (int):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryComponentUsage]
    """

    kwargs = _get_kwargs(
        id=id,
        field=field,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
) -> CategoryComponentUsage:
    """Retrieve an aggregated category component usage record

     Returns the details of a single aggregated usage record for a category component, identified by its
    database ID.

    Args:
        id (int):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryComponentUsage
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            field=field,
        )
    ).parsed
