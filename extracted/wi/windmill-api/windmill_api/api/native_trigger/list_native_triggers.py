from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_native_triggers_response_200_item import ListNativeTriggersResponse200Item
from ...models.list_native_triggers_service_name import ListNativeTriggersServiceName
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    service_name: ListNativeTriggersServiceName,
    *,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["path"] = path

    params["is_flow"] = is_flow

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/native_triggers/{service_name}/list".format(
            workspace=workspace,
            service_name=service_name,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListNativeTriggersResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListNativeTriggersResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListNativeTriggersResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: ListNativeTriggersServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Response[List["ListNativeTriggersResponse200Item"]]:
    """list native triggers

     Lists all native triggers for the specified service in the workspace.

    Args:
        workspace (str):
        service_name (ListNativeTriggersServiceName):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListNativeTriggersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    service_name: ListNativeTriggersServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Optional[List["ListNativeTriggersResponse200Item"]]:
    """list native triggers

     Lists all native triggers for the specified service in the workspace.

    Args:
        workspace (str):
        service_name (ListNativeTriggersServiceName):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListNativeTriggersResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        client=client,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: ListNativeTriggersServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Response[List["ListNativeTriggersResponse200Item"]]:
    """list native triggers

     Lists all native triggers for the specified service in the workspace.

    Args:
        workspace (str):
        service_name (ListNativeTriggersServiceName):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListNativeTriggersResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: ListNativeTriggersServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Optional[List["ListNativeTriggersResponse200Item"]]:
    """list native triggers

     Lists all native triggers for the specified service in the workspace.

    Args:
        workspace (str):
        service_name (ListNativeTriggersServiceName):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListNativeTriggersResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            client=client,
            page=page,
            per_page=per_page,
            path=path,
            is_flow=is_flow,
        )
    ).parsed
