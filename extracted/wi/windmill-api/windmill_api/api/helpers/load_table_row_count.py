from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.load_table_row_count_response_200 import LoadTableRowCountResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["search_col"] = search_col

    params["search_term"] = search_term

    params["storage"] = storage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/load_table_count/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[LoadTableRowCountResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LoadTableRowCountResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LoadTableRowCountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadTableRowCountResponse200]:
    """Load the table row count

    Args:
        workspace (str):
        path (str):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadTableRowCountResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        search_col=search_col,
        search_term=search_term,
        storage=storage,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadTableRowCountResponse200]:
    """Load the table row count

    Args:
        workspace (str):
        path (str):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadTableRowCountResponse200
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
        search_col=search_col,
        search_term=search_term,
        storage=storage,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Response[LoadTableRowCountResponse200]:
    """Load the table row count

    Args:
        workspace (str):
        path (str):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoadTableRowCountResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        search_col=search_col,
        search_term=search_term,
        storage=storage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[LoadTableRowCountResponse200]:
    """Load the table row count

    Args:
        workspace (str):
        path (str):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoadTableRowCountResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
            search_col=search_col,
            search_term=search_term,
            storage=storage,
        )
    ).parsed
