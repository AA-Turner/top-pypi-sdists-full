import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ssh_key_o_enum import SshKeyOEnum
from ...models.version_history import VersionHistory
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid_path: UUID,
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["fingerprint_md5"] = fingerprint_md5

    params["fingerprint_sha256"] = fingerprint_sha256

    params["fingerprint_sha512"] = fingerprint_sha512

    params["is_shared"] = is_shared

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["name"] = name

    params["name_exact"] = name_exact

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    json_uuid_query: Union[Unset, str] = UNSET
    if not isinstance(uuid_query, Unset):
        json_uuid_query = str(uuid_query)
    params["uuid"] = json_uuid_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/keys/{uuid_path}/history/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["VersionHistory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VersionHistory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["VersionHistory"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid_path=uuid_path,
        created=created,
        created_after=created_after,
        created_before=created_before,
        fingerprint_md5=fingerprint_md5,
        fingerprint_sha256=fingerprint_sha256,
        fingerprint_sha512=fingerprint_sha512,
        is_shared=is_shared,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
        uuid_query=uuid_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return sync_detailed(
        uuid_path=uuid_path,
        client=client,
        created=created,
        created_after=created_after,
        created_before=created_before,
        fingerprint_md5=fingerprint_md5,
        fingerprint_sha256=fingerprint_sha256,
        fingerprint_sha512=fingerprint_sha512,
        is_shared=is_shared,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
        uuid_query=uuid_query,
    ).parsed


async def asyncio_detailed(
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid_path=uuid_path,
        created=created,
        created_after=created_after,
        created_before=created_before,
        fingerprint_md5=fingerprint_md5,
        fingerprint_sha256=fingerprint_sha256,
        fingerprint_sha512=fingerprint_sha512,
        is_shared=is_shared,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
        uuid_query=uuid_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return (
        await asyncio_detailed(
            uuid_path=uuid_path,
            client=client,
            created=created,
            created_after=created_after,
            created_before=created_before,
            fingerprint_md5=fingerprint_md5,
            fingerprint_sha256=fingerprint_sha256,
            fingerprint_sha512=fingerprint_sha512,
            is_shared=is_shared,
            modified=modified,
            name=name,
            name_exact=name_exact,
            o=o,
            page=page,
            page_size=page_size,
            user_uuid=user_uuid,
            uuid_query=uuid_query,
        )
    ).parsed


def sync_all(
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid_path=uuid_path,
        created=created,
        created_after=created_after,
        created_before=created_before,
        fingerprint_md5=fingerprint_md5,
        fingerprint_sha256=fingerprint_sha256,
        fingerprint_sha512=fingerprint_sha512,
        is_shared=is_shared,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        user_uuid=user_uuid,
        uuid_query=uuid_query,
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
    uuid_path: UUID,
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    fingerprint_md5: Union[Unset, str] = UNSET,
    fingerprint_sha256: Union[Unset, str] = UNSET,
    fingerprint_sha512: Union[Unset, str] = UNSET,
    is_shared: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SshKeyOEnum]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    uuid_query: Union[Unset, UUID] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid_path (UUID):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[SshKeyOEnum]]):
        user_uuid (Union[Unset, UUID]):
        uuid_query (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid_path=uuid_path,
        created=created,
        created_after=created_after,
        created_before=created_before,
        fingerprint_md5=fingerprint_md5,
        fingerprint_sha256=fingerprint_sha256,
        fingerprint_sha512=fingerprint_sha512,
        is_shared=is_shared,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        user_uuid=user_uuid,
        uuid_query=uuid_query,
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
