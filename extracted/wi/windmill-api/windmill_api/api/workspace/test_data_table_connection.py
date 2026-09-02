from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.test_data_table_connection_response_200 import TestDataTableConnectionResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    datatable_name: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/test_datatable_connection/{datatable_name}".format(
            workspace=workspace,
            datatable_name=datatable_name,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TestDataTableConnectionResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TestDataTableConnectionResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TestDataTableConnectionResponse200]:
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
) -> Response[TestDataTableConnectionResponse200]:
    """check what the data table's database lets its role do

    Args:
        workspace (str):
        datatable_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestDataTableConnectionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
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
) -> Optional[TestDataTableConnectionResponse200]:
    """check what the data table's database lets its role do

    Args:
        workspace (str):
        datatable_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestDataTableConnectionResponse200
    """

    return sync_detailed(
        workspace=workspace,
        datatable_name=datatable_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TestDataTableConnectionResponse200]:
    """check what the data table's database lets its role do

    Args:
        workspace (str):
        datatable_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestDataTableConnectionResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[TestDataTableConnectionResponse200]:
    """check what the data table's database lets its role do

    Args:
        workspace (str):
        datatable_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestDataTableConnectionResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            datatable_name=datatable_name,
            client=client,
        )
    ).parsed
