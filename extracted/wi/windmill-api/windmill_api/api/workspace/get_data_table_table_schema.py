from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_data_table_table_schema_response_200 import GetDataTableTableSchemaResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    datatable_name: str,
    schema_name: str,
    table_name: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["datatable_name"] = datatable_name

    params["schema_name"] = schema_name

    params["table_name"] = table_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/get_datatable_table_schema".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetDataTableTableSchemaResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDataTableTableSchemaResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetDataTableTableSchemaResponse200]:
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
    datatable_name: str,
    schema_name: str,
    table_name: str,
) -> Response[GetDataTableTableSchemaResponse200]:
    """get one Datatable table schema

    Args:
        workspace (str):
        datatable_name (str):
        schema_name (str):
        table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDataTableTableSchemaResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        schema_name=schema_name,
        table_name=table_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    datatable_name: str,
    schema_name: str,
    table_name: str,
) -> Optional[GetDataTableTableSchemaResponse200]:
    """get one Datatable table schema

    Args:
        workspace (str):
        datatable_name (str):
        schema_name (str):
        table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDataTableTableSchemaResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        datatable_name=datatable_name,
        schema_name=schema_name,
        table_name=table_name,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    datatable_name: str,
    schema_name: str,
    table_name: str,
) -> Response[GetDataTableTableSchemaResponse200]:
    """get one Datatable table schema

    Args:
        workspace (str):
        datatable_name (str):
        schema_name (str):
        table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDataTableTableSchemaResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        schema_name=schema_name,
        table_name=table_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    datatable_name: str,
    schema_name: str,
    table_name: str,
) -> Optional[GetDataTableTableSchemaResponse200]:
    """get one Datatable table schema

    Args:
        workspace (str):
        datatable_name (str):
        schema_name (str):
        table_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDataTableTableSchemaResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            datatable_name=datatable_name,
            schema_name=schema_name,
            table_name=table_name,
        )
    ).parsed
