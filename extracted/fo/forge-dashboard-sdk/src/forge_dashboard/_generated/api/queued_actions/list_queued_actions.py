from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.queued_action import QueuedAction
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/queued-actions",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | list[QueuedAction] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = QueuedAction.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | list[QueuedAction]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | list[QueuedAction]]:
    """ List the signed-in user's queued actions, waiting and recently finished

     Every action the user queued to run when a rate-limited forge
    resets, oldest first: the ones still `queued`, and the
    final ones (`done`, `skipped`, `failed`) kept for 24 hours so a
    client can show the outcome in its Activity list. The same list
    rides along on GET /api/v1/dashboard as `queuedActions`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[QueuedAction]]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> Error | list[QueuedAction] | None:
    """ List the signed-in user's queued actions, waiting and recently finished

     Every action the user queued to run when a rate-limited forge
    resets, oldest first: the ones still `queued`, and the
    final ones (`done`, `skipped`, `failed`) kept for 24 hours so a
    client can show the outcome in its Activity list. The same list
    rides along on GET /api/v1/dashboard as `queuedActions`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[QueuedAction]
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | list[QueuedAction]]:
    """ List the signed-in user's queued actions, waiting and recently finished

     Every action the user queued to run when a rate-limited forge
    resets, oldest first: the ones still `queued`, and the
    final ones (`done`, `skipped`, `failed`) kept for 24 hours so a
    client can show the outcome in its Activity list. The same list
    rides along on GET /api/v1/dashboard as `queuedActions`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[QueuedAction]]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> Error | list[QueuedAction] | None:
    """ List the signed-in user's queued actions, waiting and recently finished

     Every action the user queued to run when a rate-limited forge
    resets, oldest first: the ones still `queued`, and the
    final ones (`done`, `skipped`, `failed`) kept for 24 hours so a
    client can show the outcome in its Activity list. The same list
    rides along on GET /api/v1/dashboard as `queuedActions`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[QueuedAction]
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
