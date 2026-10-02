import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    author_email: Union[Unset, str] = UNSET,
    author_fullname: Union[Unset, str] = UNSET,
    author_username: Union[Unset, str] = UNSET,
    author_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    last_published: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["author_email"] = author_email

    params["author_fullname"] = author_fullname

    params["author_username"] = author_username

    json_author_uuid: Union[Unset, str] = UNSET
    if not isinstance(author_uuid, Unset):
        json_author_uuid = str(author_uuid)
    params["author_uuid"] = json_author_uuid

    params["is_active"] = is_active

    json_last_published: Union[Unset, str] = UNSET
    if not isinstance(last_published, Unset):
        json_last_published = last_published.isoformat()
    params["last_published"] = json_last_published

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/hooks/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        return None
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    author_email: Union[Unset, str] = UNSET,
    author_fullname: Union[Unset, str] = UNSET,
    author_username: Union[Unset, str] = UNSET,
    author_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    last_published: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        author_email (Union[Unset, str]):
        author_fullname (Union[Unset, str]):
        author_username (Union[Unset, str]):
        author_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        last_published (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        author_email=author_email,
        author_fullname=author_fullname,
        author_username=author_username,
        author_uuid=author_uuid,
        is_active=is_active,
        last_published=last_published,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    author_email: Union[Unset, str] = UNSET,
    author_fullname: Union[Unset, str] = UNSET,
    author_username: Union[Unset, str] = UNSET,
    author_uuid: Union[Unset, UUID] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    last_published: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """
    Args:
        author_email (Union[Unset, str]):
        author_fullname (Union[Unset, str]):
        author_username (Union[Unset, str]):
        author_uuid (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):
        last_published (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        author_email=author_email,
        author_fullname=author_fullname,
        author_username=author_username,
        author_uuid=author_uuid,
        is_active=is_active,
        last_published=last_published,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
