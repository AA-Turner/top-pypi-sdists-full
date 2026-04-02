from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.comment import Comment
from ...models.thread_session_o_enum import ThreadSessionOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/support-comments/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Comment"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Comment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Comment"]]:
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
) -> Response[list["Comment"]]:
    """
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
        Response[list['Comment']]
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
) -> list["Comment"]:
    """
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
        list['Comment']
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
) -> Response[list["Comment"]]:
    """
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
        Response[list['Comment']]
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
) -> list["Comment"]:
    """
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
        list['Comment']
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


def sync_all(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> list["Comment"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Comment']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Comment] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        author_name=author_name,
        author_user=author_user,
        description=description,
        is_public=is_public,
        issue=issue,
        issue_uuid=issue_uuid,
        o=o,
        remote_id_is_set=remote_id_is_set,
        resource=resource,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    author_name: Union[Unset, str] = UNSET,
    author_user: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    is_public: Union[Unset, bool] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    remote_id_is_set: Union[Unset, bool] = UNSET,
    resource: Union[Unset, str] = UNSET,
) -> list["Comment"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        author_name (Union[Unset, str]):
        author_user (Union[Unset, str]):
        description (Union[Unset, str]):
        is_public (Union[Unset, bool]):
        issue (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        remote_id_is_set (Union[Unset, bool]):
        resource (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Comment']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Comment] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        author_name=author_name,
        author_user=author_user,
        description=description,
        is_public=is_public,
        issue=issue,
        issue_uuid=issue_uuid,
        o=o,
        remote_id_is_set=remote_id_is_set,
        resource=resource,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
