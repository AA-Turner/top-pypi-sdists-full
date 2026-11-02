from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_native_trigger_connections_response_200_item import ListNativeTriggerConnectionsResponse200Item
from ...models.list_native_trigger_connections_service_name import ListNativeTriggerConnectionsServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: ListNativeTriggerConnectionsServiceName,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/native_triggers/integrations/{service_name}/connections".format(
            workspace=workspace,
            service_name=service_name,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListNativeTriggerConnectionsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListNativeTriggerConnectionsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListNativeTriggerConnectionsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: ListNativeTriggerConnectionsServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["ListNativeTriggerConnectionsResponse200Item"]]:
    """list the native trigger connections of a service the caller can use

    Args:
        workspace (str):
        service_name (ListNativeTriggerConnectionsServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListNativeTriggerConnectionsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    service_name: ListNativeTriggerConnectionsServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListNativeTriggerConnectionsResponse200Item"]]:
    """list the native trigger connections of a service the caller can use

    Args:
        workspace (str):
        service_name (ListNativeTriggerConnectionsServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListNativeTriggerConnectionsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: ListNativeTriggerConnectionsServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["ListNativeTriggerConnectionsResponse200Item"]]:
    """list the native trigger connections of a service the caller can use

    Args:
        workspace (str):
        service_name (ListNativeTriggerConnectionsServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListNativeTriggerConnectionsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: ListNativeTriggerConnectionsServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["ListNativeTriggerConnectionsResponse200Item"]]:
    """list the native trigger connections of a service the caller can use

    Args:
        workspace (str):
        service_name (ListNativeTriggerConnectionsServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListNativeTriggerConnectionsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            client=client,
        )
    ).parsed
