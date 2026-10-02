from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_reprovision_response import MatrixReprovisionResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/matrix/reprovision/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MatrixReprovisionResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 202:
        response_202 = MatrixReprovisionResponse.from_dict(response.json())

        return response_202
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MatrixReprovisionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[MatrixReprovisionResponse]:
    """Reprovision all active Matrix rooms on a new homeserver

     Resets all active rooms to 'creating' state and re-queues them for provisioning. Also resets all
    user profiles. Staff only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixReprovisionResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> MatrixReprovisionResponse:
    """Reprovision all active Matrix rooms on a new homeserver

     Resets all active rooms to 'creating' state and re-queues them for provisioning. Also resets all
    user profiles. Staff only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixReprovisionResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[MatrixReprovisionResponse]:
    """Reprovision all active Matrix rooms on a new homeserver

     Resets all active rooms to 'creating' state and re-queues them for provisioning. Also resets all
    user profiles. Staff only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixReprovisionResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> MatrixReprovisionResponse:
    """Reprovision all active Matrix rooms on a new homeserver

     Resets all active rooms to 'creating' state and re-queues them for provisioning. Also resets all
    user profiles. Staff only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixReprovisionResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
