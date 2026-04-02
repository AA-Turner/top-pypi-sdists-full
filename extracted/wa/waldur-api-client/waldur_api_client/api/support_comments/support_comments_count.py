from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.thread_session_o_enum import ThreadSessionOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["author_name"] = author_name

    params["author_user"] = author_user

    params["description"] = description

    params["is_public"] = is_public

    params["issue"] = issue

    json_issue_uuid: Union[Unset, str] = UNSET
    if not isinstance(issue_uuid, Unset):
        json_issue_uuid = str(issue_uuid)
    params["issue_uuid"] = json_issue_uuid

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["remote_id_is_set"] = remote_id_is_set

    params["resource"] = resource

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/support-comments/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        author_name=author_name,
        author_user=author_user,
        description=description,
        is_public=is_public,
        issue=issue,
        issue_uuid=issue_uuid,
        o=o,
        page=page,
        page_size=page_size,
        remote_id_is_set=remote_id_is_set,
        resource=resource,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        author_name=author_name,
        author_user=author_user,
        description=description,
        is_public=is_public,
        issue=issue,
        issue_uuid=issue_uuid,
        o=o,
        page=page,
        page_size=page_size,
        remote_id_is_set=remote_id_is_set,
        resource=resource,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        author_name=author_name,
        author_user=author_user,
        description=description,
        is_public=is_public,
        issue=issue,
        issue_uuid=issue_uuid,
        o=o,
        page=page,
        page_size=page_size,
        remote_id_is_set=remote_id_is_set,
        resource=resource,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            author_name=author_name,
            author_user=author_user,
            description=description,
            is_public=is_public,
            issue=issue,
            issue_uuid=issue_uuid,
            o=o,
            page=page,
            page_size=page_size,
            remote_id_is_set=remote_id_is_set,
            resource=resource,
        )
    ).parsed
