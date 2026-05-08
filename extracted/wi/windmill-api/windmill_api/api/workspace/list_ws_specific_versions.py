from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_ws_specific_versions_kind import ListWsSpecificVersionsKind
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    kind: ListWsSpecificVersionsKind,
    path: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_kind = kind.value

    params["kind"] = json_kind

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/list_ws_specific_versions".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List[str]]:
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
    kind: ListWsSpecificVersionsKind,
    path: str,
) -> Response[List[str]]:
    """list workspace ids that have a version of the given item

    Args:
        workspace (str):
        kind (ListWsSpecificVersionsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
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
    kind: ListWsSpecificVersionsKind,
    path: str,
) -> Optional[List[str]]:
    """list workspace ids that have a version of the given item

    Args:
        workspace (str):
        kind (ListWsSpecificVersionsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        kind=kind,
        path=path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: ListWsSpecificVersionsKind,
    path: str,
) -> Response[List[str]]:
    """list workspace ids that have a version of the given item

    Args:
        workspace (str):
        kind (ListWsSpecificVersionsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: ListWsSpecificVersionsKind,
    path: str,
) -> Optional[List[str]]:
    """list workspace ids that have a version of the given item

    Args:
        workspace (str):
        kind (ListWsSpecificVersionsKind):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            kind=kind,
            path=path,
        )
    ).parsed
