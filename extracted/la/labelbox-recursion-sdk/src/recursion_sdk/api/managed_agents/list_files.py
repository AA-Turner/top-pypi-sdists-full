from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_files_source import ListFilesSource
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_file_list_response import ManagedAgentsFileListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    scope_session_id: str | Unset = UNSET,
    file_ids: list[str] | Unset = UNSET,
    source: ListFilesSource | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["scope_session_id"] = scope_session_id

    json_file_ids: list[str] | Unset = UNSET
    if not isinstance(file_ids, Unset):
        json_file_ids = file_ids


    params["file_ids"] = json_file_ids

    json_source: str | Unset = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/files",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsFileListResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    scope_session_id: str | Unset = UNSET,
    file_ids: list[str] | Unset = UNSET,
    source: ListFilesSource | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse]:
    """ List files

     Returns the caller organization's files, newest first, one page at a time: up to limit files
    (default 200, at most 1000) and a next_page_token while more follow. Deleted files are omitted; an
    expired file stays listed, with expires_at in the past, until the reclaim pass takes it after the
    grace, so a client that wants only attachable files filters on expires_at. Filter to one session's
    outputs with scope_session_id or by source. A file_ids lookup (at most 100 ids) is always one page
    and cannot be combined with limit or page_token.

    Args:
        scope_session_id (str | Unset): Return only the files this session produced.
        file_ids (list[str] | Unset): Return only these files, comma-separated or repeated, for
            resolving a session's attachments in one read. At most 100 ids, answered as one page:
            limit and page_token are refused alongside it, an id that names nothing visible is left
            out rather than reported, and a file_ids that names no id at all answers no files.
        source (ListFilesSource | Unset): Return only uploads or only session outputs.
        limit (int | Unset): Maximum files to return per page; defaults to 200, newest first.
        page_token (str | Unset): Opaque cursor from a previous response's next_page_token. Send
            it with the same filters and limit the previous page used; a token issued for a different
            query, organization, or collection is refused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse]
     """


    kwargs = _get_kwargs(
        scope_session_id=scope_session_id,
file_ids=file_ids,
source=source,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    scope_session_id: str | Unset = UNSET,
    file_ids: list[str] | Unset = UNSET,
    source: ListFilesSource | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse | None:
    """ List files

     Returns the caller organization's files, newest first, one page at a time: up to limit files
    (default 200, at most 1000) and a next_page_token while more follow. Deleted files are omitted; an
    expired file stays listed, with expires_at in the past, until the reclaim pass takes it after the
    grace, so a client that wants only attachable files filters on expires_at. Filter to one session's
    outputs with scope_session_id or by source. A file_ids lookup (at most 100 ids) is always one page
    and cannot be combined with limit or page_token.

    Args:
        scope_session_id (str | Unset): Return only the files this session produced.
        file_ids (list[str] | Unset): Return only these files, comma-separated or repeated, for
            resolving a session's attachments in one read. At most 100 ids, answered as one page:
            limit and page_token are refused alongside it, an id that names nothing visible is left
            out rather than reported, and a file_ids that names no id at all answers no files.
        source (ListFilesSource | Unset): Return only uploads or only session outputs.
        limit (int | Unset): Maximum files to return per page; defaults to 200, newest first.
        page_token (str | Unset): Opaque cursor from a previous response's next_page_token. Send
            it with the same filters and limit the previous page used; a token issued for a different
            query, organization, or collection is refused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse
     """


    return sync_detailed(
        client=client,
scope_session_id=scope_session_id,
file_ids=file_ids,
source=source,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    scope_session_id: str | Unset = UNSET,
    file_ids: list[str] | Unset = UNSET,
    source: ListFilesSource | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse]:
    """ List files

     Returns the caller organization's files, newest first, one page at a time: up to limit files
    (default 200, at most 1000) and a next_page_token while more follow. Deleted files are omitted; an
    expired file stays listed, with expires_at in the past, until the reclaim pass takes it after the
    grace, so a client that wants only attachable files filters on expires_at. Filter to one session's
    outputs with scope_session_id or by source. A file_ids lookup (at most 100 ids) is always one page
    and cannot be combined with limit or page_token.

    Args:
        scope_session_id (str | Unset): Return only the files this session produced.
        file_ids (list[str] | Unset): Return only these files, comma-separated or repeated, for
            resolving a session's attachments in one read. At most 100 ids, answered as one page:
            limit and page_token are refused alongside it, an id that names nothing visible is left
            out rather than reported, and a file_ids that names no id at all answers no files.
        source (ListFilesSource | Unset): Return only uploads or only session outputs.
        limit (int | Unset): Maximum files to return per page; defaults to 200, newest first.
        page_token (str | Unset): Opaque cursor from a previous response's next_page_token. Send
            it with the same filters and limit the previous page used; a token issued for a different
            query, organization, or collection is refused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse]
     """


    kwargs = _get_kwargs(
        scope_session_id=scope_session_id,
file_ids=file_ids,
source=source,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    scope_session_id: str | Unset = UNSET,
    file_ids: list[str] | Unset = UNSET,
    source: ListFilesSource | Unset = UNSET,
    limit: int | Unset = UNSET,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse | None:
    """ List files

     Returns the caller organization's files, newest first, one page at a time: up to limit files
    (default 200, at most 1000) and a next_page_token while more follow. Deleted files are omitted; an
    expired file stays listed, with expires_at in the past, until the reclaim pass takes it after the
    grace, so a client that wants only attachable files filters on expires_at. Filter to one session's
    outputs with scope_session_id or by source. A file_ids lookup (at most 100 ids) is always one page
    and cannot be combined with limit or page_token.

    Args:
        scope_session_id (str | Unset): Return only the files this session produced.
        file_ids (list[str] | Unset): Return only these files, comma-separated or repeated, for
            resolving a session's attachments in one read. At most 100 ids, answered as one page:
            limit and page_token are refused alongside it, an id that names nothing visible is left
            out rather than reported, and a file_ids that names no id at all answers no files.
        source (ListFilesSource | Unset): Return only uploads or only session outputs.
        limit (int | Unset): Maximum files to return per page; defaults to 200, newest first.
        page_token (str | Unset): Opaque cursor from a previous response's next_page_token. Send
            it with the same filters and limit the previous page used; a token issued for a different
            query, organization, or collection is refused.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsFileListResponse
     """


    return (await asyncio_detailed(
        client=client,
scope_session_id=scope_session_id,
file_ids=file_ids,
source=source,
limit=limit,
page_token=page_token,

    )).parsed
