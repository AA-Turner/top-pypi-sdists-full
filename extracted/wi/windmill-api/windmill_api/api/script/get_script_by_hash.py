from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_script_by_hash_response_200 import GetScriptByHashResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    hash_: str,
    *,
    with_starred_info: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["with_starred_info"] = with_starred_info

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/scripts/get/h/{hash}".format(
            workspace=workspace,
            hash=hash_,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetScriptByHashResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetScriptByHashResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetScriptByHashResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    with_starred_info: Union[Unset, None, bool] = UNSET,
) -> Response[GetScriptByHashResponse200]:
    """get script by hash

    Args:
        workspace (str):
        hash_ (str):
        with_starred_info (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetScriptByHashResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        hash_=hash_,
        with_starred_info=with_starred_info,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    with_starred_info: Union[Unset, None, bool] = UNSET,
) -> Optional[GetScriptByHashResponse200]:
    """get script by hash

    Args:
        workspace (str):
        hash_ (str):
        with_starred_info (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetScriptByHashResponse200
    """

    return sync_detailed(
        workspace=workspace,
        hash_=hash_,
        client=client,
        with_starred_info=with_starred_info,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    with_starred_info: Union[Unset, None, bool] = UNSET,
) -> Response[GetScriptByHashResponse200]:
    """get script by hash

    Args:
        workspace (str):
        hash_ (str):
        with_starred_info (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetScriptByHashResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        hash_=hash_,
        with_starred_info=with_starred_info,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    with_starred_info: Union[Unset, None, bool] = UNSET,
) -> Optional[GetScriptByHashResponse200]:
    """get script by hash

    Args:
        workspace (str):
        hash_ (str):
        with_starred_info (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetScriptByHashResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            hash_=hash_,
            client=client,
            with_starred_info=with_starred_info,
        )
    ).parsed
