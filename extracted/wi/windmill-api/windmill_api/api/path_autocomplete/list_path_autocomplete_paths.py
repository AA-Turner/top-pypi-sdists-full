from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_path_autocomplete_paths_response_200 import ListPathAutocompletePathsResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/path_autocomplete/list_paths".format(
            workspace=workspace,
        ),
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
) -> Response[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPathAutocompletePathsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPathAutocompletePathsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPathAutocompletePathsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListPathAutocompletePathsResponse200]:
    """list all paths in a workspace for client-side autocomplete

     Returns the flat list of all item paths visible to the caller across
    scripts, flows, apps, raw apps, variables, and resources. Intended to
    feed an entirely client-side path autocomplete UI: the frontend fetches
    once (server caches per workspace for 60s) and performs all prefix/segment
    computation locally. Capped at 20,000 paths (5,000 per table).

    Args:
        workspace (str):

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
        )
    ).parsed
