from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_trigger_history_response_200_item import ListTriggerHistoryResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    trigger_kind: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["trigger_kind"] = trigger_kind

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/triggers_history/list".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListTriggerHistoryResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListTriggerHistoryResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListTriggerHistoryResponse200Item"]]:
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
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    trigger_kind: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
) -> Response[List["ListTriggerHistoryResponse200Item"]]:
    """list the history of schedule and trigger modifications

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        trigger_kind (Union[Unset, None, str]):
        path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListTriggerHistoryResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        per_page=per_page,
        trigger_kind=trigger_kind,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    trigger_kind: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListTriggerHistoryResponse200Item"]]:
    """list the history of schedule and trigger modifications

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        trigger_kind (Union[Unset, None, str]):
        path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListTriggerHistoryResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        page=page,
        per_page=per_page,
        trigger_kind=trigger_kind,
        path=path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    trigger_kind: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
) -> Response[List["ListTriggerHistoryResponse200Item"]]:
    """list the history of schedule and trigger modifications

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        trigger_kind (Union[Unset, None, str]):
        path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListTriggerHistoryResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        page=page,
        per_page=per_page,
        trigger_kind=trigger_kind,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    trigger_kind: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListTriggerHistoryResponse200Item"]]:
    """list the history of schedule and trigger modifications

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        trigger_kind (Union[Unset, None, str]):
        path (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListTriggerHistoryResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            page=page,
            per_page=per_page,
            trigger_kind=trigger_kind,
            path=path,
        )
    ).parsed
