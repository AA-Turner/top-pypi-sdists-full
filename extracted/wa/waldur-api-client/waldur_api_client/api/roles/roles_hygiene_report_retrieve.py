from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.role_hygiene_report import RoleHygieneReport
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/roles/hygiene_report/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> RoleHygieneReport:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RoleHygieneReport.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RoleHygieneReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[RoleHygieneReport]:
    """Role hygiene report

     Staff-only. Reports roles whose name is not a machine code, whose scope or organization binding is
    wrong, that are silently global, or that carry permissions inert for their scope. Read-only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RoleHygieneReport]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> RoleHygieneReport:
    """Role hygiene report

     Staff-only. Reports roles whose name is not a machine code, whose scope or organization binding is
    wrong, that are silently global, or that carry permissions inert for their scope. Read-only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RoleHygieneReport
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[RoleHygieneReport]:
    """Role hygiene report

     Staff-only. Reports roles whose name is not a machine code, whose scope or organization binding is
    wrong, that are silently global, or that carry permissions inert for their scope. Read-only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RoleHygieneReport]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> RoleHygieneReport:
    """Role hygiene report

     Staff-only. Reports roles whose name is not a machine code, whose scope or organization binding is
    wrong, that are silently global, or that carry permissions inert for their scope. Read-only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RoleHygieneReport
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
