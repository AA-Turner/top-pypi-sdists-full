from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    include_default: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["include_default"] = include_default

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/get_secondary_storage_names".format(
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
    include_default: Union[Unset, None, bool] = False,
) -> Response[List[str]]:
    """get secondary storage names

    Args:
        workspace (str):
        include_default (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        include_default=include_default,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_default: Union[Unset, None, bool] = False,
) -> Optional[List[str]]:
    """get secondary storage names

    Args:
        workspace (str):
        include_default (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        include_default=include_default,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_default: Union[Unset, None, bool] = False,
) -> Response[List[str]]:
    """get secondary storage names

    Args:
        workspace (str):
        include_default (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        include_default=include_default,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_default: Union[Unset, None, bool] = False,
) -> Optional[List[str]]:
    """get secondary storage names

    Args:
        workspace (str):
        include_default (Union[Unset, None, bool]):

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
            include_default=include_default,
        )
    ).parsed
