from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.ready import Ready
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/readyz",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Ready | None:
    if response.status_code == 200:
        response_200 = Ready.from_dict(response.json())



        return response_200

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Ready]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | Ready]:
    """ Readiness

     Answers 200 once the server can actually serve: the database answers
    a ping with its schema in place, and the first dashboard refresh has
    completed, or 30 seconds have passed since it started. The wait is
    bounded because how fast a forge answers is how fresh the data is,
    not whether the server can serve: a slow or unreachable forge must not
    keep the container unready. A refresh that finished with a forge
    unreachable counts, and a forge going unreachable afterwards never
    turns this into a 503. See forges[].reachable on the dashboard
    response for that. Before any account has signed in there is no
    refresh to wait for, so only the database is checked.

    The database ping gets 2 seconds, less than the HEALTHCHECK's own 5,
    so a database that doesn't answer turns into a 503 instead of a hung
    probe. The ping's result, pass or fail, is reused for about 3
    seconds, so probes arriving every second don't each reach the
    database. On SIGTERM this answers 503 ("shutting down") at once, and
    the server waits a drain period (`SHUTDOWN_DRAIN`, default 5 seconds)
    before it stops accepting connections, so a router that polls this
    path stops sending traffic first.

    The container's HEALTHCHECK probes this path (`/healthz` stays the
    cheap liveness answer), so Docker's single health state and Compose's
    `depends_on: condition: service_healthy` mean "ready", not just
    "started".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Ready]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> Error | Ready | None:
    """ Readiness

     Answers 200 once the server can actually serve: the database answers
    a ping with its schema in place, and the first dashboard refresh has
    completed, or 30 seconds have passed since it started. The wait is
    bounded because how fast a forge answers is how fresh the data is,
    not whether the server can serve: a slow or unreachable forge must not
    keep the container unready. A refresh that finished with a forge
    unreachable counts, and a forge going unreachable afterwards never
    turns this into a 503. See forges[].reachable on the dashboard
    response for that. Before any account has signed in there is no
    refresh to wait for, so only the database is checked.

    The database ping gets 2 seconds, less than the HEALTHCHECK's own 5,
    so a database that doesn't answer turns into a 503 instead of a hung
    probe. The ping's result, pass or fail, is reused for about 3
    seconds, so probes arriving every second don't each reach the
    database. On SIGTERM this answers 503 ("shutting down") at once, and
    the server waits a drain period (`SHUTDOWN_DRAIN`, default 5 seconds)
    before it stops accepting connections, so a router that polls this
    path stops sending traffic first.

    The container's HEALTHCHECK probes this path (`/healthz` stays the
    cheap liveness answer), so Docker's single health state and Compose's
    `depends_on: condition: service_healthy` mean "ready", not just
    "started".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Ready
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | Ready]:
    """ Readiness

     Answers 200 once the server can actually serve: the database answers
    a ping with its schema in place, and the first dashboard refresh has
    completed, or 30 seconds have passed since it started. The wait is
    bounded because how fast a forge answers is how fresh the data is,
    not whether the server can serve: a slow or unreachable forge must not
    keep the container unready. A refresh that finished with a forge
    unreachable counts, and a forge going unreachable afterwards never
    turns this into a 503. See forges[].reachable on the dashboard
    response for that. Before any account has signed in there is no
    refresh to wait for, so only the database is checked.

    The database ping gets 2 seconds, less than the HEALTHCHECK's own 5,
    so a database that doesn't answer turns into a 503 instead of a hung
    probe. The ping's result, pass or fail, is reused for about 3
    seconds, so probes arriving every second don't each reach the
    database. On SIGTERM this answers 503 ("shutting down") at once, and
    the server waits a drain period (`SHUTDOWN_DRAIN`, default 5 seconds)
    before it stops accepting connections, so a router that polls this
    path stops sending traffic first.

    The container's HEALTHCHECK probes this path (`/healthz` stays the
    cheap liveness answer), so Docker's single health state and Compose's
    `depends_on: condition: service_healthy` mean "ready", not just
    "started".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Ready]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> Error | Ready | None:
    """ Readiness

     Answers 200 once the server can actually serve: the database answers
    a ping with its schema in place, and the first dashboard refresh has
    completed, or 30 seconds have passed since it started. The wait is
    bounded because how fast a forge answers is how fresh the data is,
    not whether the server can serve: a slow or unreachable forge must not
    keep the container unready. A refresh that finished with a forge
    unreachable counts, and a forge going unreachable afterwards never
    turns this into a 503. See forges[].reachable on the dashboard
    response for that. Before any account has signed in there is no
    refresh to wait for, so only the database is checked.

    The database ping gets 2 seconds, less than the HEALTHCHECK's own 5,
    so a database that doesn't answer turns into a 503 instead of a hung
    probe. The ping's result, pass or fail, is reused for about 3
    seconds, so probes arriving every second don't each reach the
    database. On SIGTERM this answers 503 ("shutting down") at once, and
    the server waits a drain period (`SHUTDOWN_DRAIN`, default 5 seconds)
    before it stops accepting connections, so a router that polls this
    path stops sending traffic first.

    The container's HEALTHCHECK probes this path (`/healthz` stays the
    cheap liveness answer), so Docker's single health state and Compose's
    `depends_on: condition: service_healthy` mean "ready", not just
    "started".

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Ready
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
