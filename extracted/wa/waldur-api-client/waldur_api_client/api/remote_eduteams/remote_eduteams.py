from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_eduteams_request_request import RemoteEduteamsRequestRequest
from ...models.remote_eduteams_uuid import RemoteEduteamsUUID
from ...types import Response


def _get_kwargs(
    *,
    body: RemoteEduteamsRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/remote-eduteams/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> RemoteEduteamsUUID:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RemoteEduteamsUUID.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RemoteEduteamsUUID]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RemoteEduteamsRequestRequest,
) -> Response[RemoteEduteamsUUID]:
    """Allows to pull user details from remote eduTEAMS instance.

    Args:
        body (RemoteEduteamsRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoteEduteamsUUID]
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
    body: RemoteEduteamsRequestRequest,
) -> RemoteEduteamsUUID:
    """Allows to pull user details from remote eduTEAMS instance.

    Args:
        body (RemoteEduteamsRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoteEduteamsUUID
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RemoteEduteamsRequestRequest,
) -> Response[RemoteEduteamsUUID]:
    """Allows to pull user details from remote eduTEAMS instance.

    Args:
        body (RemoteEduteamsRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoteEduteamsUUID]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RemoteEduteamsRequestRequest,
) -> RemoteEduteamsUUID:
    """Allows to pull user details from remote eduTEAMS instance.

    Args:
        body (RemoteEduteamsRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoteEduteamsUUID
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
