from http import HTTPStatus
from typing import Any, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_room_open import MatrixRoomOpen
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/matrix/rooms/{uuid}/open/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, MatrixRoomOpen]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MatrixRoomOpen.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, MatrixRoomOpen]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, MatrixRoomOpen]]:
    """Open a chat room's conversation

     Returns the Matrix room ID to a current member of the room, accepting their pending invite. Other
    callers get 403; a room that is not active gets 409.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixRoomOpen]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Union[Any, MatrixRoomOpen]:
    """Open a chat room's conversation

     Returns the Matrix room ID to a current member of the room, accepting their pending invite. Other
    callers get 403; a room that is not active gets 409.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixRoomOpen]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, MatrixRoomOpen]]:
    """Open a chat room's conversation

     Returns the Matrix room ID to a current member of the room, accepting their pending invite. Other
    callers get 403; a room that is not active gets 409.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixRoomOpen]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Union[Any, MatrixRoomOpen]:
    """Open a chat room's conversation

     Returns the Matrix room ID to a current member of the room, accepting their pending invite. Other
    callers get 403; a room that is not active gets 409.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixRoomOpen]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
