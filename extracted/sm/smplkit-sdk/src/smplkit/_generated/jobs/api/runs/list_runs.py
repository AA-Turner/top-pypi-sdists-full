from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.run_list_response import RunListResponse
from ...types import Unset


def _get_kwargs(
    *,
    filterjob: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterjob: None | str | Unset
    if isinstance(filterjob, Unset):
        json_filterjob = UNSET
    else:
        json_filterjob = filterjob
    params["filter[job]"] = json_filterjob

    json_pagesize: int | None | Unset
    if isinstance(pagesize, Unset):
        json_pagesize = UNSET
    else:
        json_pagesize = pagesize
    params["page[size]"] = json_pagesize

    json_pageafter: None | str | Unset
    if isinstance(pageafter, Unset):
        json_pageafter = UNSET
    else:
        json_pageafter = pageafter
    params["page[after]"] = json_pageafter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/runs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RunListResponse | None:
    if response.status_code == 200:
        response_200 = RunListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RunListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
) -> Response[RunListResponse]:
    """List Runs

     List runs for this account, newest first (cursor paginated).

    Use `filter[job]={id}` for a single job's run history.

    Args:
        filterjob (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunListResponse]
    """

    kwargs = _get_kwargs(
        filterjob=filterjob,
        pagesize=pagesize,
        pageafter=pageafter,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
) -> RunListResponse | None:
    """List Runs

     List runs for this account, newest first (cursor paginated).

    Use `filter[job]={id}` for a single job's run history.

    Args:
        filterjob (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunListResponse
    """

    return sync_detailed(
        client=client,
        filterjob=filterjob,
        pagesize=pagesize,
        pageafter=pageafter,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
) -> Response[RunListResponse]:
    """List Runs

     List runs for this account, newest first (cursor paginated).

    Use `filter[job]={id}` for a single job's run history.

    Args:
        filterjob (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunListResponse]
    """

    kwargs = _get_kwargs(
        filterjob=filterjob,
        pagesize=pagesize,
        pageafter=pageafter,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
) -> RunListResponse | None:
    """List Runs

     List runs for this account, newest first (cursor paginated).

    Use `filter[job]={id}` for a single job's run history.

    Args:
        filterjob (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterjob=filterjob,
            pagesize=pagesize,
            pageafter=pageafter,
        )
    ).parsed
