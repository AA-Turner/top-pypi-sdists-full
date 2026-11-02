from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.filter_state import FilterState
from typing import cast



def _get_kwargs(
    *,
    body: FilterState,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/settings/filter-state",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FilterState,

) -> Response[Any | Error]:
    """ Save the signed-in user's own dashboard/Insights filter state

     A dedicated, lightweight save separate from the main
    PUT /api/v1/settings — filters change on nearly every click, a
    mismatch for that endpoint's "always a full form submit"
    convention. The body replaces the saved state entirely,
    the same "always a full submit, just of a much smaller and
    much more frequent thing" shape as the main settings PUT, not a
    partial patch. Filters.js's own client-side code decides when
    to call this: immediately for a discrete control, debounced
    while the user is still typing in the free-text Title filter.
    A signed-in browser session only: a personal API token is refused
    with 403, so a script or agent can't change the filters the user
    sees. Each save is logged with the user agent.

    Args:
        body (FilterState): The dashboard/Insights filter bar's own saved shape (and the
            Branches page's status, forge, advisories and search, in a `branches` group) —
            whatever the frontend's `$lib/filters` `loadState`/`saveState` already produce
            client-side (shared forge/repo/label/author/title/created/
            updated/groupBy, plus the two board-owned extras with no
            equivalent on the other entity type). `shared.label`,
            `shared.repo` (forge-qualified, `forge:owner/name`) and
            `shared.author` are each one lowercase value, or several separated
            by a newline: the filter matches an item with any of them, and a
            single value saved before they took several still reads as a list
            of one. At most 20 values and 1000 characters in each, with no
            control character other than the separator; a save over either is
            refused. This server stores and
            returns it verbatim, byte for byte, and apart from those limits never parses or
            validates its shape — the same "opaque blob, not this layer's
            concern" treatment WebAuthnCeremonyOptions above gets, so a
            client-side shape change here never needs a matching spec change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: FilterState,

) -> Any | Error | None:
    """ Save the signed-in user's own dashboard/Insights filter state

     A dedicated, lightweight save separate from the main
    PUT /api/v1/settings — filters change on nearly every click, a
    mismatch for that endpoint's "always a full form submit"
    convention. The body replaces the saved state entirely,
    the same "always a full submit, just of a much smaller and
    much more frequent thing" shape as the main settings PUT, not a
    partial patch. Filters.js's own client-side code decides when
    to call this: immediately for a discrete control, debounced
    while the user is still typing in the free-text Title filter.
    A signed-in browser session only: a personal API token is refused
    with 403, so a script or agent can't change the filters the user
    sees. Each save is logged with the user agent.

    Args:
        body (FilterState): The dashboard/Insights filter bar's own saved shape (and the
            Branches page's status, forge, advisories and search, in a `branches` group) —
            whatever the frontend's `$lib/filters` `loadState`/`saveState` already produce
            client-side (shared forge/repo/label/author/title/created/
            updated/groupBy, plus the two board-owned extras with no
            equivalent on the other entity type). `shared.label`,
            `shared.repo` (forge-qualified, `forge:owner/name`) and
            `shared.author` are each one lowercase value, or several separated
            by a newline: the filter matches an item with any of them, and a
            single value saved before they took several still reads as a list
            of one. At most 20 values and 1000 characters in each, with no
            control character other than the separator; a save over either is
            refused. This server stores and
            returns it verbatim, byte for byte, and apart from those limits never parses or
            validates its shape — the same "opaque blob, not this layer's
            concern" treatment WebAuthnCeremonyOptions above gets, so a
            client-side shape change here never needs a matching spec change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FilterState,

) -> Response[Any | Error]:
    """ Save the signed-in user's own dashboard/Insights filter state

     A dedicated, lightweight save separate from the main
    PUT /api/v1/settings — filters change on nearly every click, a
    mismatch for that endpoint's "always a full form submit"
    convention. The body replaces the saved state entirely,
    the same "always a full submit, just of a much smaller and
    much more frequent thing" shape as the main settings PUT, not a
    partial patch. Filters.js's own client-side code decides when
    to call this: immediately for a discrete control, debounced
    while the user is still typing in the free-text Title filter.
    A signed-in browser session only: a personal API token is refused
    with 403, so a script or agent can't change the filters the user
    sees. Each save is logged with the user agent.

    Args:
        body (FilterState): The dashboard/Insights filter bar's own saved shape (and the
            Branches page's status, forge, advisories and search, in a `branches` group) —
            whatever the frontend's `$lib/filters` `loadState`/`saveState` already produce
            client-side (shared forge/repo/label/author/title/created/
            updated/groupBy, plus the two board-owned extras with no
            equivalent on the other entity type). `shared.label`,
            `shared.repo` (forge-qualified, `forge:owner/name`) and
            `shared.author` are each one lowercase value, or several separated
            by a newline: the filter matches an item with any of them, and a
            single value saved before they took several still reads as a list
            of one. At most 20 values and 1000 characters in each, with no
            control character other than the separator; a save over either is
            refused. This server stores and
            returns it verbatim, byte for byte, and apart from those limits never parses or
            validates its shape — the same "opaque blob, not this layer's
            concern" treatment WebAuthnCeremonyOptions above gets, so a
            client-side shape change here never needs a matching spec change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FilterState,

) -> Any | Error | None:
    """ Save the signed-in user's own dashboard/Insights filter state

     A dedicated, lightweight save separate from the main
    PUT /api/v1/settings — filters change on nearly every click, a
    mismatch for that endpoint's "always a full form submit"
    convention. The body replaces the saved state entirely,
    the same "always a full submit, just of a much smaller and
    much more frequent thing" shape as the main settings PUT, not a
    partial patch. Filters.js's own client-side code decides when
    to call this: immediately for a discrete control, debounced
    while the user is still typing in the free-text Title filter.
    A signed-in browser session only: a personal API token is refused
    with 403, so a script or agent can't change the filters the user
    sees. Each save is logged with the user agent.

    Args:
        body (FilterState): The dashboard/Insights filter bar's own saved shape (and the
            Branches page's status, forge, advisories and search, in a `branches` group) —
            whatever the frontend's `$lib/filters` `loadState`/`saveState` already produce
            client-side (shared forge/repo/label/author/title/created/
            updated/groupBy, plus the two board-owned extras with no
            equivalent on the other entity type). `shared.label`,
            `shared.repo` (forge-qualified, `forge:owner/name`) and
            `shared.author` are each one lowercase value, or several separated
            by a newline: the filter matches an item with any of them, and a
            single value saved before they took several still reads as a list
            of one. At most 20 values and 1000 characters in each, with no
            control character other than the separator; a save over either is
            refused. This server stores and
            returns it verbatim, byte for byte, and apart from those limits never parses or
            validates its shape — the same "opaque blob, not this layer's
            concern" treatment WebAuthnCeremonyOptions above gets, so a
            client-side shape change here never needs a matching spec change.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
