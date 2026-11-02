from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.stream_watch_request import StreamWatchRequest
from typing import cast



def _get_kwargs(
    *,
    body: StreamWatchRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/dashboard/stream/watch",
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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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
    body: StreamWatchRequest,

) -> Response[Any | Error]:
    """ Choose which job lists a dashboard stream sends

     Replaces the set of pull requests and default branches whose job
    lists the stream named by `streamId` sends as `run` events.
    The server lists a subject when it is newly watched, when its row
    in a new snapshot changed (CI state, check counts, or a branch's
    run), and when `refresh` is true. Nothing else costs a forge
    request. A failed listing is sent as an event with `error` set,
    and every snapshot after it tries again, changed or not, until a
    listing works.

    A listing is one event for each workflow run attempt the subject
    holds, then one with `gone` set for each run attempt the last
    listing sent and this one lacks. The last event of a listing has
    `final` set. A rerun keeps its run id and takes a new attempt, so
    its event carries a new `key` and the first attempt's key comes
    back as gone. The event is the JSON of the `RunEvent` schema.

    Args:
        body (StreamWatchRequest):

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
    body: StreamWatchRequest,

) -> Any | Error | None:
    """ Choose which job lists a dashboard stream sends

     Replaces the set of pull requests and default branches whose job
    lists the stream named by `streamId` sends as `run` events.
    The server lists a subject when it is newly watched, when its row
    in a new snapshot changed (CI state, check counts, or a branch's
    run), and when `refresh` is true. Nothing else costs a forge
    request. A failed listing is sent as an event with `error` set,
    and every snapshot after it tries again, changed or not, until a
    listing works.

    A listing is one event for each workflow run attempt the subject
    holds, then one with `gone` set for each run attempt the last
    listing sent and this one lacks. The last event of a listing has
    `final` set. A rerun keeps its run id and takes a new attempt, so
    its event carries a new `key` and the first attempt's key comes
    back as gone. The event is the JSON of the `RunEvent` schema.

    Args:
        body (StreamWatchRequest):

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
    body: StreamWatchRequest,

) -> Response[Any | Error]:
    """ Choose which job lists a dashboard stream sends

     Replaces the set of pull requests and default branches whose job
    lists the stream named by `streamId` sends as `run` events.
    The server lists a subject when it is newly watched, when its row
    in a new snapshot changed (CI state, check counts, or a branch's
    run), and when `refresh` is true. Nothing else costs a forge
    request. A failed listing is sent as an event with `error` set,
    and every snapshot after it tries again, changed or not, until a
    listing works.

    A listing is one event for each workflow run attempt the subject
    holds, then one with `gone` set for each run attempt the last
    listing sent and this one lacks. The last event of a listing has
    `final` set. A rerun keeps its run id and takes a new attempt, so
    its event carries a new `key` and the first attempt's key comes
    back as gone. The event is the JSON of the `RunEvent` schema.

    Args:
        body (StreamWatchRequest):

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
    body: StreamWatchRequest,

) -> Any | Error | None:
    """ Choose which job lists a dashboard stream sends

     Replaces the set of pull requests and default branches whose job
    lists the stream named by `streamId` sends as `run` events.
    The server lists a subject when it is newly watched, when its row
    in a new snapshot changed (CI state, check counts, or a branch's
    run), and when `refresh` is true. Nothing else costs a forge
    request. A failed listing is sent as an event with `error` set,
    and every snapshot after it tries again, changed or not, until a
    listing works.

    A listing is one event for each workflow run attempt the subject
    holds, then one with `gone` set for each run attempt the last
    listing sent and this one lacks. The last event of a listing has
    `final` set. A rerun keeps its run id and takes a new attempt, so
    its event carries a new `key` and the first attempt's key comes
    back as gone. The event is the JSON of the `RunEvent` schema.

    Args:
        body (StreamWatchRequest):

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
