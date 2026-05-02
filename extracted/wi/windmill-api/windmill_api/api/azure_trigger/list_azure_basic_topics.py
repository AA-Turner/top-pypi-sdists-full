from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_azure_basic_topics_response_200_item import ListAzureBasicTopicsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/w/{workspace}/azure_triggers/basic/topics/list/{path}".format(
            workspace=workspace,
            path=path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListAzureBasicTopicsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAzureBasicTopicsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListAzureBasicTopicsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["ListAzureBasicTopicsResponse200Item"]]:
    """list Basic Event Grid topics + system topics the service principal can access

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAzureBasicTopicsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListAzureBasicTopicsResponse200Item"]]:
    """list Basic Event Grid topics + system topics the service principal can access

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAzureBasicTopicsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["ListAzureBasicTopicsResponse200Item"]]:
    """list Basic Event Grid topics + system topics the service principal can access

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAzureBasicTopicsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListAzureBasicTopicsResponse200Item"]]:
    """list Basic Event Grid topics + system topics the service principal can access

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAzureBasicTopicsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
        )
    ).parsed
