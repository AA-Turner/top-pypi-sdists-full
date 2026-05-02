from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_jobs_index_response_200 import SearchJobsIndexResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    search_query: str,
    pagination_offset: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["search_query"] = search_query

    params["pagination_offset"] = pagination_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/srch/w/{workspace}/index/search/job".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SearchJobsIndexResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchJobsIndexResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SearchJobsIndexResponse200]:
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
    search_query: str,
    pagination_offset: Union[Unset, None, int] = UNSET,
) -> Response[SearchJobsIndexResponse200]:
    """Search through jobs with a string query

    Args:
        workspace (str):
        search_query (str):
        pagination_offset (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchJobsIndexResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search_query=search_query,
        pagination_offset=pagination_offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    pagination_offset: Union[Unset, None, int] = UNSET,
) -> Optional[SearchJobsIndexResponse200]:
    """Search through jobs with a string query

    Args:
        workspace (str):
        search_query (str):
        pagination_offset (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchJobsIndexResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        search_query=search_query,
        pagination_offset=pagination_offset,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    pagination_offset: Union[Unset, None, int] = UNSET,
) -> Response[SearchJobsIndexResponse200]:
    """Search through jobs with a string query

    Args:
        workspace (str):
        search_query (str):
        pagination_offset (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchJobsIndexResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        search_query=search_query,
        pagination_offset=pagination_offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    search_query: str,
    pagination_offset: Union[Unset, None, int] = UNSET,
) -> Optional[SearchJobsIndexResponse200]:
    """Search through jobs with a string query

    Args:
        workspace (str):
        search_query (str):
        pagination_offset (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SearchJobsIndexResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            search_query=search_query,
            pagination_offset=pagination_offset,
        )
    ).parsed
