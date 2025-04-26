from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    offset: Union[Unset, None, float] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    sort_col: Union[Unset, None, str] = UNSET,
    sort_desc: Union[Unset, None, bool] = UNSET,
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["offset"] = offset

    params["limit"] = limit

    params["sort_col"] = sort_col

    params["sort_desc"] = sort_desc

    params["search_col"] = search_col

    params["search_term"] = search_term

    params["storage"] = storage

    params["csv_separator"] = csv_separator

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/load_csv_preview/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    offset: Union[Unset, None, float] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    sort_col: Union[Unset, None, str] = UNSET,
    sort_desc: Union[Unset, None, bool] = UNSET,
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Load a preview of a csv file

    Args:
        workspace (str):
        path (str):
        offset (Union[Unset, None, float]):
        limit (Union[Unset, None, float]):
        sort_col (Union[Unset, None, str]):
        sort_desc (Union[Unset, None, bool]):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        offset=offset,
        limit=limit,
        sort_col=sort_col,
        sort_desc=sort_desc,
        search_col=search_col,
        search_term=search_term,
        storage=storage,
        csv_separator=csv_separator,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, None, float] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    sort_col: Union[Unset, None, str] = UNSET,
    sort_desc: Union[Unset, None, bool] = UNSET,
    search_col: Union[Unset, None, str] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    storage: Union[Unset, None, str] = UNSET,
    csv_separator: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Load a preview of a csv file

    Args:
        workspace (str):
        path (str):
        offset (Union[Unset, None, float]):
        limit (Union[Unset, None, float]):
        sort_col (Union[Unset, None, str]):
        sort_desc (Union[Unset, None, bool]):
        search_col (Union[Unset, None, str]):
        search_term (Union[Unset, None, str]):
        storage (Union[Unset, None, str]):
        csv_separator (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        offset=offset,
        limit=limit,
        sort_col=sort_col,
        sort_desc=sort_desc,
        search_col=search_col,
        search_term=search_term,
        storage=storage,
        csv_separator=csv_separator,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
