from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_datatable_migration_json_body import CreateDatatableMigrationJsonBody
from ...models.create_datatable_migration_response_200 import CreateDatatableMigrationResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    datatable_name: str,
    *,
    json_body: CreateDatatableMigrationJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/create_datatable_migration/{datatable_name}".format(
            workspace=workspace,
            datatable_name=datatable_name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CreateDatatableMigrationResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateDatatableMigrationResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateDatatableMigrationResponse200]:
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
    json_body: CreateDatatableMigrationJsonBody,
) -> Response[CreateDatatableMigrationResponse200]:
    """create a single datatable migration (version generated server-side)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (CreateDatatableMigrationJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDatatableMigrationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        json_body=json_body,
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
    json_body: CreateDatatableMigrationJsonBody,
) -> Optional[CreateDatatableMigrationResponse200]:
    """create a single datatable migration (version generated server-side)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (CreateDatatableMigrationJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDatatableMigrationResponse200
    """

    return sync_detailed(
        workspace=workspace,
        datatable_name=datatable_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateDatatableMigrationJsonBody,
) -> Response[CreateDatatableMigrationResponse200]:
    """create a single datatable migration (version generated server-side)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (CreateDatatableMigrationJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDatatableMigrationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateDatatableMigrationJsonBody,
) -> Optional[CreateDatatableMigrationResponse200]:
    """create a single datatable migration (version generated server-side)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (CreateDatatableMigrationJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateDatatableMigrationResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            datatable_name=datatable_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
