from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_path_autocomplete_paths_response_200 import ListPathAutocompletePathsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    force: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/path_autocomplete/list_paths".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListPathAutocompletePathsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListPathAutocompletePathsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListPathAutocompletePathsResponse200]:
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
    force: Union[Unset, None, bool] = UNSET,
) -> Response[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPathAutocompletePathsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = UNSET,
) -> Optional[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPathAutocompletePathsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = UNSET,
) -> Response[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPathAutocompletePathsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = UNSET,
) -> Optional[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPathAutocompletePathsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            force=force,
        )
    ).parsed
