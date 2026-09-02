from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.count_runnables_by_owner_response_200 import CountRunnablesByOwnerResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    kinds: Union[Unset, None, str] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["kinds"] = kinds

    params["include_without_main"] = include_without_main

    params["include_draft_only"] = include_draft_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/runnables/counts".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CountRunnablesByOwnerResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CountRunnablesByOwnerResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CountRunnablesByOwnerResponse200]:
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
    kinds: Union[Unset, None, str] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Response[CountRunnablesByOwnerResponse200]:
    """count runnables per owner (folder or user space)

    Args:
        workspace (str):
        kinds (Union[Unset, None, str]):
        include_without_main (Union[Unset, None, bool]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CountRunnablesByOwnerResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kinds=kinds,
        include_without_main=include_without_main,
        include_draft_only=include_draft_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kinds: Union[Unset, None, str] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Optional[CountRunnablesByOwnerResponse200]:
    """count runnables per owner (folder or user space)

    Args:
        workspace (str):
        kinds (Union[Unset, None, str]):
        include_without_main (Union[Unset, None, bool]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CountRunnablesByOwnerResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        kinds=kinds,
        include_without_main=include_without_main,
        include_draft_only=include_draft_only,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kinds: Union[Unset, None, str] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Response[CountRunnablesByOwnerResponse200]:
    """count runnables per owner (folder or user space)

    Args:
        workspace (str):
        kinds (Union[Unset, None, str]):
        include_without_main (Union[Unset, None, bool]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CountRunnablesByOwnerResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kinds=kinds,
        include_without_main=include_without_main,
        include_draft_only=include_draft_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kinds: Union[Unset, None, str] = UNSET,
    include_without_main: Union[Unset, None, bool] = UNSET,
    include_draft_only: Union[Unset, None, bool] = UNSET,
) -> Optional[CountRunnablesByOwnerResponse200]:
    """count runnables per owner (folder or user space)

    Args:
        workspace (str):
        kinds (Union[Unset, None, str]):
        include_without_main (Union[Unset, None, bool]):
        include_draft_only (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CountRunnablesByOwnerResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            kinds=kinds,
            include_without_main=include_without_main,
            include_draft_only=include_draft_only,
        )
    ).parsed
