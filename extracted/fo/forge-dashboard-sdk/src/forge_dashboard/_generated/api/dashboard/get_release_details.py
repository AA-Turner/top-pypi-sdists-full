from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.forge import Forge
from ...models.release_details import ReleaseDetails
from typing import cast



def _get_kwargs(
    *,
    forge: Forge,
    full_name: str,
    tag: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_forge = forge.value
    params["forge"] = json_forge

    params["fullName"] = full_name

    params["tag"] = tag


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/releases/details",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ReleaseDetails | None:
    if response.status_code == 200:
        response_200 = ReleaseDetails.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ReleaseDetails]:
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
    tag: str,

) -> Response[Error | ReleaseDetails]:
    """ Read a published release's title and notes, on demand

     What the release dialog on the Main branches page shows for a
    repository's latest published release: its title, when it was
    published, its notes and the thumbs reactions on them. Fetched live on
    every call, never as part of GET /api/v1/main-branches' snapshot, so a
    release nobody opens costs no budget.

    GitHub answers with one GraphQL query. Only GitHub rows carry a latest
    release today, so a Forgejo repository is a 400.

    The notes are Markdown exactly as the forge stores them (`format` is
    always `markdown`). The server neither converts nor sanitises them, so
    a client must render them with raw HTML disabled. They are cut at
    20,000 characters (`truncated`), and a reaction names at most its
    first 10 people while `count` is the full number.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. A tag that has no published release is a 404, and so is a draft,
    a pre-release or a release with no publish date.

    Args:
        forge (Forge):
        full_name (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ReleaseDetails]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
tag=tag,

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
    tag: str,

) -> Error | ReleaseDetails | None:
    """ Read a published release's title and notes, on demand

     What the release dialog on the Main branches page shows for a
    repository's latest published release: its title, when it was
    published, its notes and the thumbs reactions on them. Fetched live on
    every call, never as part of GET /api/v1/main-branches' snapshot, so a
    release nobody opens costs no budget.

    GitHub answers with one GraphQL query. Only GitHub rows carry a latest
    release today, so a Forgejo repository is a 400.

    The notes are Markdown exactly as the forge stores them (`format` is
    always `markdown`). The server neither converts nor sanitises them, so
    a client must render them with raw HTML disabled. They are cut at
    20,000 characters (`truncated`), and a reaction names at most its
    first 10 people while `count` is the full number.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. A tag that has no published release is a 404, and so is a draft,
    a pre-release or a release with no publish date.

    Args:
        forge (Forge):
        full_name (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ReleaseDetails
     """


    return sync_detailed(
        client=client,
forge=forge,
full_name=full_name,
tag=tag,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    tag: str,

) -> Response[Error | ReleaseDetails]:
    """ Read a published release's title and notes, on demand

     What the release dialog on the Main branches page shows for a
    repository's latest published release: its title, when it was
    published, its notes and the thumbs reactions on them. Fetched live on
    every call, never as part of GET /api/v1/main-branches' snapshot, so a
    release nobody opens costs no budget.

    GitHub answers with one GraphQL query. Only GitHub rows carry a latest
    release today, so a Forgejo repository is a 400.

    The notes are Markdown exactly as the forge stores them (`format` is
    always `markdown`). The server neither converts nor sanitises them, so
    a client must render them with raw HTML disabled. They are cut at
    20,000 characters (`truncated`), and a reaction names at most its
    first 10 people while `count` is the full number.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. A tag that has no published release is a 404, and so is a draft,
    a pre-release or a release with no publish date.

    Args:
        forge (Forge):
        full_name (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ReleaseDetails]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
tag=tag,

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
    tag: str,

) -> Error | ReleaseDetails | None:
    """ Read a published release's title and notes, on demand

     What the release dialog on the Main branches page shows for a
    repository's latest published release: its title, when it was
    published, its notes and the thumbs reactions on them. Fetched live on
    every call, never as part of GET /api/v1/main-branches' snapshot, so a
    release nobody opens costs no budget.

    GitHub answers with one GraphQL query. Only GitHub rows carry a latest
    release today, so a Forgejo repository is a 400.

    The notes are Markdown exactly as the forge stores them (`format` is
    always `markdown`). The server neither converts nor sanitises them, so
    a client must render them with raw HTML disabled. They are cut at
    20,000 characters (`truncated`), and a reaction names at most its
    first 10 people while `count` is the full number.

    The error answers are those of GET /api/v1/pull-requests/details, with
    the same codes. A tag that has no published release is a 404, and so is a draft,
    a pre-release or a release with no publish date.

    Args:
        forge (Forge):
        full_name (str):
        tag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ReleaseDetails
     """


    return (await asyncio_detailed(
        client=client,
forge=forge,
full_name=full_name,
tag=tag,

    )).parsed
