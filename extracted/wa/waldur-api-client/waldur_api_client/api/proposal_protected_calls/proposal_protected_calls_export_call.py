from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_export_parameters_request import CallExportParametersRequest
from ...models.call_export_response import CallExportResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: CallExportParametersRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/export_call/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CallExportResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CallExportResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CallExportResponse]:
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
    body: CallExportParametersRequest,
) -> Response[CallExportResponse]:
    """Export call configuration

     Export the call's configuration as a portable document that import_call can recreate on another
    portal. Offerings, plans, checklists and roles are referenced by name. Proposals, reviews, reviewer
    pools, assignments and user references are never exported.

    Args:
        uuid (UUID):
        body (CallExportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallExportResponse]
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
    body: CallExportParametersRequest,
) -> CallExportResponse:
    """Export call configuration

     Export the call's configuration as a portable document that import_call can recreate on another
    portal. Offerings, plans, checklists and roles are referenced by name. Proposals, reviews, reviewer
    pools, assignments and user references are never exported.

    Args:
        uuid (UUID):
        body (CallExportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallExportResponse
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
    body: CallExportParametersRequest,
) -> Response[CallExportResponse]:
    """Export call configuration

     Export the call's configuration as a portable document that import_call can recreate on another
    portal. Offerings, plans, checklists and roles are referenced by name. Proposals, reviews, reviewer
    pools, assignments and user references are never exported.

    Args:
        uuid (UUID):
        body (CallExportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallExportResponse]
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
    body: CallExportParametersRequest,
) -> CallExportResponse:
    """Export call configuration

     Export the call's configuration as a portable document that import_call can recreate on another
    portal. Offerings, plans, checklists and roles are referenced by name. Proposals, reviews, reviewer
    pools, assignments and user references are never exported.

    Args:
        uuid (UUID):
        body (CallExportParametersRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallExportResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
