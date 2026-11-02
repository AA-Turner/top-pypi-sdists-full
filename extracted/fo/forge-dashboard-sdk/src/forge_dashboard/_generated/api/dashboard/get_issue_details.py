from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.forge import Forge
from ...models.issue_details import IssueDetails
from typing import cast



def _get_kwargs(
    *,
    forge: Forge,
    full_name: str,
    number: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_forge = forge.value
    params["forge"] = json_forge

    params["fullName"] = full_name

    params["number"] = number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/issues/details",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | IssueDetails | None:
    if response.status_code == 200:
        response_200 = IssueDetails.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | IssueDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Response[Error | IssueDetails]:
    """ Read an issue's description, comments and reactions, on demand

     What the issue dialog shows: the description, the conversation in
    order, and the thumbs up and thumbs down reactions on each with who
    gave them. The same shape and rules as GET /api/v1/pull-requests/details
    without the release notes, which only a pull request has. Fetched live
    on every call, never as part of GET /api/v1/dashboard's snapshot.

    GitHub answers with one GraphQL query. Forgejo costs one call for the
    issue, one for its comments, one for the description's reactions and
    one for each comment's reactions (up to 50), so the reaction calls run
    at most eight at a time and stop at the first rate limit.

    Every text is Markdown exactly as the forge stores it (`format` is
    always `markdown`). The server neither converts nor sanitises it, so a
    client must render it with raw HTML disabled. Each text is cut at
    20,000 characters (`truncated`), the conversation keeps its first 50
    comments (`commentsTruncated`, with the full `commentCount`), and a
    reaction names at most its first 10 people while `count` is the full
    number. An avatar is the forge's own URL, passed through unchanged and
    never proxied.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. An issue that doesn't exist is a 404, and a forge that
    can't be read is an error, never an empty thread.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | IssueDetails]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
number=number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Error | IssueDetails | None:
    """ Read an issue's description, comments and reactions, on demand

     What the issue dialog shows: the description, the conversation in
    order, and the thumbs up and thumbs down reactions on each with who
    gave them. The same shape and rules as GET /api/v1/pull-requests/details
    without the release notes, which only a pull request has. Fetched live
    on every call, never as part of GET /api/v1/dashboard's snapshot.

    GitHub answers with one GraphQL query. Forgejo costs one call for the
    issue, one for its comments, one for the description's reactions and
    one for each comment's reactions (up to 50), so the reaction calls run
    at most eight at a time and stop at the first rate limit.

    Every text is Markdown exactly as the forge stores it (`format` is
    always `markdown`). The server neither converts nor sanitises it, so a
    client must render it with raw HTML disabled. Each text is cut at
    20,000 characters (`truncated`), the conversation keeps its first 50
    comments (`commentsTruncated`, with the full `commentCount`), and a
    reaction names at most its first 10 people while `count` is the full
    number. An avatar is the forge's own URL, passed through unchanged and
    never proxied.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. An issue that doesn't exist is a 404, and a forge that
    can't be read is an error, never an empty thread.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | IssueDetails
     """


    return sync_detailed(
        client=client,
forge=forge,
full_name=full_name,
number=number,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Response[Error | IssueDetails]:
    """ Read an issue's description, comments and reactions, on demand

     What the issue dialog shows: the description, the conversation in
    order, and the thumbs up and thumbs down reactions on each with who
    gave them. The same shape and rules as GET /api/v1/pull-requests/details
    without the release notes, which only a pull request has. Fetched live
    on every call, never as part of GET /api/v1/dashboard's snapshot.

    GitHub answers with one GraphQL query. Forgejo costs one call for the
    issue, one for its comments, one for the description's reactions and
    one for each comment's reactions (up to 50), so the reaction calls run
    at most eight at a time and stop at the first rate limit.

    Every text is Markdown exactly as the forge stores it (`format` is
    always `markdown`). The server neither converts nor sanitises it, so a
    client must render it with raw HTML disabled. Each text is cut at
    20,000 characters (`truncated`), the conversation keeps its first 50
    comments (`commentsTruncated`, with the full `commentCount`), and a
    reaction names at most its first 10 people while `count` is the full
    number. An avatar is the forge's own URL, passed through unchanged and
    never proxied.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. An issue that doesn't exist is a 404, and a forge that
    can't be read is an error, never an empty thread.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | IssueDetails]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
number=number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Error | IssueDetails | None:
    """ Read an issue's description, comments and reactions, on demand

     What the issue dialog shows: the description, the conversation in
    order, and the thumbs up and thumbs down reactions on each with who
    gave them. The same shape and rules as GET /api/v1/pull-requests/details
    without the release notes, which only a pull request has. Fetched live
    on every call, never as part of GET /api/v1/dashboard's snapshot.

    GitHub answers with one GraphQL query. Forgejo costs one call for the
    issue, one for its comments, one for the description's reactions and
    one for each comment's reactions (up to 50), so the reaction calls run
    at most eight at a time and stop at the first rate limit.

    Every text is Markdown exactly as the forge stores it (`format` is
    always `markdown`). The server neither converts nor sanitises it, so a
    client must render it with raw HTML disabled. Each text is cut at
    20,000 characters (`truncated`), the conversation keeps its first 50
    comments (`commentsTruncated`, with the full `commentCount`), and a
    reaction names at most its first 10 people while `count` is the full
    number. An avatar is the forge's own URL, passed through unchanged and
    never proxied.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. An issue that doesn't exist is a 404, and a forge that
    can't be read is an error, never an empty thread.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | IssueDetails
     """


    return (await asyncio_detailed(
        client=client,
forge=forge,
full_name=full_name,
number=number,

    )).parsed
