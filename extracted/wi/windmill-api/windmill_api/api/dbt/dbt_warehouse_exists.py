from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    workspace: str,
    name: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/dbt/warehouse_exists/{name}".format(
            workspace=workspace,
            name=name,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """check that a dbt warehouse is configured, without resolving it

     Job-scoped: needs a job token. For a project bringing its own `profiles.yml`, which names a
    warehouse only to say where its assets belong and never opens the connection.

    Args:
        workspace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """check that a dbt warehouse is configured, without resolving it

     Job-scoped: needs a job token. For a project bringing its own `profiles.yml`, which names a
    warehouse only to say where its assets belong and never opens the connection.

    Args:
        workspace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
