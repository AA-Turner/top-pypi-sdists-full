from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_external_instance_pg_databases_response_200 import ListExternalInstancePgDatabasesResponse200
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/settings/external_instance_pg/databases",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListExternalInstancePgDatabasesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListExternalInstancePgDatabasesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListExternalInstancePgDatabasesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListExternalInstancePgDatabasesResponse200]:
    """Lists the databases Windmill created on the external instance cluster, with the workspaces whose
    data tables, Ducklake catalogs or pending fork cleanups use each

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListExternalInstancePgDatabasesResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListExternalInstancePgDatabasesResponse200]:
    """Lists the databases Windmill created on the external instance cluster, with the workspaces whose
    data tables, Ducklake catalogs or pending fork cleanups use each

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListExternalInstancePgDatabasesResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListExternalInstancePgDatabasesResponse200]:
    """Lists the databases Windmill created on the external instance cluster, with the workspaces whose
    data tables, Ducklake catalogs or pending fork cleanups use each

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListExternalInstancePgDatabasesResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListExternalInstancePgDatabasesResponse200]:
    """Lists the databases Windmill created on the external instance cluster, with the workspaces whose
    data tables, Ducklake catalogs or pending fork cleanups use each

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListExternalInstancePgDatabasesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
