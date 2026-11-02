from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rollback_datatable_migrations_response_200 import RollbackDatatableMigrationsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    datatable_name: str,
    *,
    only: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["only"] = only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/rollback_datatable_migrations/{datatable_name}".format(
            workspace=workspace,
            datatable_name=datatable_name,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RollbackDatatableMigrationsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RollbackDatatableMigrationsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RollbackDatatableMigrationsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    only: Union[Unset, None, int] = UNSET,
) -> Response[RollbackDatatableMigrationsResponse200]:
    """roll back the most recently applied migration on a datatable

    Args:
        workspace (str):
        datatable_name (str):
        only (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RollbackDatatableMigrationsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        only=only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    only: Union[Unset, None, int] = UNSET,
) -> Optional[RollbackDatatableMigrationsResponse200]:
    """roll back the most recently applied migration on a datatable

    Args:
        workspace (str):
        datatable_name (str):
        only (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RollbackDatatableMigrationsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        datatable_name=datatable_name,
        client=client,
        only=only,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    only: Union[Unset, None, int] = UNSET,
) -> Response[RollbackDatatableMigrationsResponse200]:
    """roll back the most recently applied migration on a datatable

    Args:
        workspace (str):
        datatable_name (str):
        only (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RollbackDatatableMigrationsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        only=only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    only: Union[Unset, None, int] = UNSET,
) -> Optional[RollbackDatatableMigrationsResponse200]:
    """roll back the most recently applied migration on a datatable

    Args:
        workspace (str):
        datatable_name (str):
        only (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RollbackDatatableMigrationsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            datatable_name=datatable_name,
            client=client,
            only=only,
        )
    ).parsed
