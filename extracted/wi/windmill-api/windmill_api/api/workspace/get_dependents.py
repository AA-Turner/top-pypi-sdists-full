from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_dependents_response_200_item import GetDependentsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    imported_path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/get_dependents/{imported_path}".format(
            workspace=workspace,
            imported_path=imported_path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["GetDependentsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetDependentsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["GetDependentsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    imported_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GetDependentsResponse200Item"]]:
    """get dependents of an imported path

    Args:
        workspace (str):
        imported_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetDependentsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        imported_path=imported_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    imported_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GetDependentsResponse200Item"]]:
    """get dependents of an imported path

    Args:
        workspace (str):
        imported_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetDependentsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        imported_path=imported_path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    imported_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GetDependentsResponse200Item"]]:
    """get dependents of an imported path

    Args:
        workspace (str):
        imported_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetDependentsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        imported_path=imported_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    imported_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GetDependentsResponse200Item"]]:
    """get dependents of an imported path

    Args:
        workspace (str):
        imported_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetDependentsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            imported_path=imported_path,
            client=client,
        )
    ).parsed
