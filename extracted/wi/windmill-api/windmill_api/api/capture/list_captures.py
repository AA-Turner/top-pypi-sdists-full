from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_captures_response_200_item import ListCapturesResponse200Item
from ...models.list_captures_runnable_kind import ListCapturesRunnableKind
from ...models.list_captures_trigger_kind import ListCapturesTriggerKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    runnable_kind: ListCapturesRunnableKind,
    path: str,
    *,
    trigger_kind: Union[Unset, None, ListCapturesTriggerKind] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_trigger_kind: Union[Unset, None, str] = UNSET
    if not isinstance(trigger_kind, Unset):
        json_trigger_kind = trigger_kind.value if trigger_kind else None

    params["trigger_kind"] = json_trigger_kind

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/capture/list/{runnable_kind}/{path}".format(
            workspace=workspace,
            runnable_kind=runnable_kind,
            path=path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListCapturesResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListCapturesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListCapturesResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    runnable_kind: ListCapturesRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_kind: Union[Unset, None, ListCapturesTriggerKind] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List["ListCapturesResponse200Item"]]:
    """list captures for a script or flow

    Args:
        workspace (str):
        runnable_kind (ListCapturesRunnableKind):
        path (str):
        trigger_kind (Union[Unset, None, ListCapturesTriggerKind]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListCapturesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        trigger_kind=trigger_kind,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    runnable_kind: ListCapturesRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_kind: Union[Unset, None, ListCapturesTriggerKind] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List["ListCapturesResponse200Item"]]:
    """list captures for a script or flow

    Args:
        workspace (str):
        runnable_kind (ListCapturesRunnableKind):
        path (str):
        trigger_kind (Union[Unset, None, ListCapturesTriggerKind]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListCapturesResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        client=client,
        trigger_kind=trigger_kind,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    runnable_kind: ListCapturesRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_kind: Union[Unset, None, ListCapturesTriggerKind] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List["ListCapturesResponse200Item"]]:
    """list captures for a script or flow

    Args:
        workspace (str):
        runnable_kind (ListCapturesRunnableKind):
        path (str):
        trigger_kind (Union[Unset, None, ListCapturesTriggerKind]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListCapturesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        trigger_kind=trigger_kind,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    runnable_kind: ListCapturesRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_kind: Union[Unset, None, ListCapturesTriggerKind] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List["ListCapturesResponse200Item"]]:
    """list captures for a script or flow

    Args:
        workspace (str):
        runnable_kind (ListCapturesRunnableKind):
        path (str):
        trigger_kind (Union[Unset, None, ListCapturesTriggerKind]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListCapturesResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            runnable_kind=runnable_kind,
            path=path,
            client=client,
            trigger_kind=trigger_kind,
            page=page,
            per_page=per_page,
        )
    ).parsed
