from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_conversation_messages_response_200_item import ListConversationMessagesResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    conversation_id: str,
    *,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["after_id"] = after_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/flow_conversations/{conversation_id}/messages".format(
            workspace=workspace,
            conversation_id=conversation_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListConversationMessagesResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListConversationMessagesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListConversationMessagesResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    conversation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_id: Union[Unset, None, str] = UNSET,
) -> Response[List["ListConversationMessagesResponse200Item"]]:
    """list conversation messages

    Args:
        workspace (str):
        conversation_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        after_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListConversationMessagesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        conversation_id=conversation_id,
        page=page,
        per_page=per_page,
        after_id=after_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    conversation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_id: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListConversationMessagesResponse200Item"]]:
    """list conversation messages

    Args:
        workspace (str):
        conversation_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        after_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListConversationMessagesResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        conversation_id=conversation_id,
        client=client,
        page=page,
        per_page=per_page,
        after_id=after_id,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    conversation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_id: Union[Unset, None, str] = UNSET,
) -> Response[List["ListConversationMessagesResponse200Item"]]:
    """list conversation messages

    Args:
        workspace (str):
        conversation_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        after_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListConversationMessagesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        conversation_id=conversation_id,
        page=page,
        per_page=per_page,
        after_id=after_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    conversation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    after_id: Union[Unset, None, str] = UNSET,
) -> Optional[List["ListConversationMessagesResponse200Item"]]:
    """list conversation messages

    Args:
        workspace (str):
        conversation_id (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        after_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListConversationMessagesResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            conversation_id=conversation_id,
            client=client,
            page=page,
            per_page=per_page,
            after_id=after_id,
        )
    ).parsed
