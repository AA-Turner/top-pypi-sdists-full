from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_instance_datatable_roles_cluster import ListInstanceDatatableRolesCluster
from ...models.list_instance_datatable_roles_response_200_item import ListInstanceDatatableRolesResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cluster: Union[Unset, None, ListInstanceDatatableRolesCluster] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_cluster: Union[Unset, None, str] = UNSET
    if not isinstance(cluster, Unset):
        json_cluster = cluster.value if cluster else None

    params["cluster"] = json_cluster

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/settings/datatable_roles",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListInstanceDatatableRolesResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListInstanceDatatableRolesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListInstanceDatatableRolesResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, None, ListInstanceDatatableRolesCluster] = UNSET,
) -> Response[List["ListInstanceDatatableRolesResponse200Item"]]:
    """list the data table roles of one Windmill-managed Postgres cluster

    Args:
        cluster (Union[Unset, None, ListInstanceDatatableRolesCluster]): The Windmill-managed
            Postgres cluster a data table role is a login on: Windmill's own (behind `instance` data
            tables) or the external instance cluster (behind `external_instance` ones). Defaults to
            `instance`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListInstanceDatatableRolesResponse200Item']]
    """

    kwargs = _get_kwargs(
        cluster=cluster,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, None, ListInstanceDatatableRolesCluster] = UNSET,
) -> Optional[List["ListInstanceDatatableRolesResponse200Item"]]:
    """list the data table roles of one Windmill-managed Postgres cluster

    Args:
        cluster (Union[Unset, None, ListInstanceDatatableRolesCluster]): The Windmill-managed
            Postgres cluster a data table role is a login on: Windmill's own (behind `instance` data
            tables) or the external instance cluster (behind `external_instance` ones). Defaults to
            `instance`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListInstanceDatatableRolesResponse200Item']
    """

    return sync_detailed(
        client=client,
        cluster=cluster,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, None, ListInstanceDatatableRolesCluster] = UNSET,
) -> Response[List["ListInstanceDatatableRolesResponse200Item"]]:
    """list the data table roles of one Windmill-managed Postgres cluster

    Args:
        cluster (Union[Unset, None, ListInstanceDatatableRolesCluster]): The Windmill-managed
            Postgres cluster a data table role is a login on: Windmill's own (behind `instance` data
            tables) or the external instance cluster (behind `external_instance` ones). Defaults to
            `instance`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListInstanceDatatableRolesResponse200Item']]
    """

    kwargs = _get_kwargs(
        cluster=cluster,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, None, ListInstanceDatatableRolesCluster] = UNSET,
) -> Optional[List["ListInstanceDatatableRolesResponse200Item"]]:
    """list the data table roles of one Windmill-managed Postgres cluster

    Args:
        cluster (Union[Unset, None, ListInstanceDatatableRolesCluster]): The Windmill-managed
            Postgres cluster a data table role is a login on: Windmill's own (behind `instance` data
            tables) or the external instance cluster (behind `external_instance` ones). Defaults to
            `instance`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListInstanceDatatableRolesResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            cluster=cluster,
        )
    ).parsed
