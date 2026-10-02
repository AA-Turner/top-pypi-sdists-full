from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.diagnose_connectivity_request_request import DiagnoseConnectivityRequestRequest
from ...models.diagnose_connectivity_response import DiagnoseConnectivityResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: DiagnoseConnectivityRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openstack-instances/{uuid}/diagnose_connectivity/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> DiagnoseConnectivityResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DiagnoseConnectivityResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DiagnoseConnectivityResponse]:
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
    body: DiagnoseConnectivityRequestRequest,
) -> Response[DiagnoseConnectivityResponse]:
    """Diagnose connectivity

     Walks the wiring that connects this instance to the requested target (default 'external') and
    returns a per-check report computed from Waldur's already-pulled state — no live OpenStack call. Use
    to triage 'VM can't reach the internet' or 'VIP doesn't work' tickets in one click.

    Args:
        uuid (UUID):
        body (DiagnoseConnectivityRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnoseConnectivityResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: DiagnoseConnectivityRequestRequest,
) -> DiagnoseConnectivityResponse:
    """Diagnose connectivity

     Walks the wiring that connects this instance to the requested target (default 'external') and
    returns a per-check report computed from Waldur's already-pulled state — no live OpenStack call. Use
    to triage 'VM can't reach the internet' or 'VIP doesn't work' tickets in one click.

    Args:
        uuid (UUID):
        body (DiagnoseConnectivityRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnoseConnectivityResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: DiagnoseConnectivityRequestRequest,
) -> Response[DiagnoseConnectivityResponse]:
    """Diagnose connectivity

     Walks the wiring that connects this instance to the requested target (default 'external') and
    returns a per-check report computed from Waldur's already-pulled state — no live OpenStack call. Use
    to triage 'VM can't reach the internet' or 'VIP doesn't work' tickets in one click.

    Args:
        uuid (UUID):
        body (DiagnoseConnectivityRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiagnoseConnectivityResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: DiagnoseConnectivityRequestRequest,
) -> DiagnoseConnectivityResponse:
    """Diagnose connectivity

     Walks the wiring that connects this instance to the requested target (default 'external') and
    returns a per-check report computed from Waldur's already-pulled state — no live OpenStack call. Use
    to triage 'VM can't reach the internet' or 'VIP doesn't work' tickets in one click.

    Args:
        uuid (UUID):
        body (DiagnoseConnectivityRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiagnoseConnectivityResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
