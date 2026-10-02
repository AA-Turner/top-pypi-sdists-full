from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_call_request_request import DuplicateCallRequestRequest
from ...models.protected_call import ProtectedCall
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: DuplicateCallRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/duplicate/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ProtectedCall:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ProtectedCall.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProtectedCall]:
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
    body: DuplicateCallRequestRequest,
) -> Response[ProtectedCall]:
    """Duplicate a call. The new call inherits the source call's configuration (offerings, rounds, workflow
    steps, resource templates, role mappings, documents, and COI/matching/assignment/applicant-
    visibility settings) and starts in draft state. Proposals, reviews, team permissions, and reviewer-
    pool memberships are not copied.

    Args:
        uuid (UUID):
        body (DuplicateCallRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProtectedCall]
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
    body: DuplicateCallRequestRequest,
) -> ProtectedCall:
    """Duplicate a call. The new call inherits the source call's configuration (offerings, rounds, workflow
    steps, resource templates, role mappings, documents, and COI/matching/assignment/applicant-
    visibility settings) and starts in draft state. Proposals, reviews, team permissions, and reviewer-
    pool memberships are not copied.

    Args:
        uuid (UUID):
        body (DuplicateCallRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProtectedCall
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
    body: DuplicateCallRequestRequest,
) -> Response[ProtectedCall]:
    """Duplicate a call. The new call inherits the source call's configuration (offerings, rounds, workflow
    steps, resource templates, role mappings, documents, and COI/matching/assignment/applicant-
    visibility settings) and starts in draft state. Proposals, reviews, team permissions, and reviewer-
    pool memberships are not copied.

    Args:
        uuid (UUID):
        body (DuplicateCallRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProtectedCall]
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
    body: DuplicateCallRequestRequest,
) -> ProtectedCall:
    """Duplicate a call. The new call inherits the source call's configuration (offerings, rounds, workflow
    steps, resource templates, role mappings, documents, and COI/matching/assignment/applicant-
    visibility settings) and starts in draft state. Proposals, reviews, team permissions, and reviewer-
    pool memberships are not copied.

    Args:
        uuid (UUID):
        body (DuplicateCallRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProtectedCall
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
