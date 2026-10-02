from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.extend_deadline_request_request import ExtendDeadlineRequestRequest
from ...models.extend_deadline_response import ExtendDeadlineResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ExtendDeadlineRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/assignment-batches/{uuid}/extend-deadline/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ExtendDeadlineResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ExtendDeadlineResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExtendDeadlineResponse]:
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
    body: ExtendDeadlineRequestRequest,
) -> Response[ExtendDeadlineResponse]:
    """Extend or modify the expiration date for an assignment batch. Can reactivate expired batches by
    setting a future deadline.

    Args:
        uuid (UUID):
        body (ExtendDeadlineRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtendDeadlineResponse]
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
    body: ExtendDeadlineRequestRequest,
) -> ExtendDeadlineResponse:
    """Extend or modify the expiration date for an assignment batch. Can reactivate expired batches by
    setting a future deadline.

    Args:
        uuid (UUID):
        body (ExtendDeadlineRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtendDeadlineResponse
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
    body: ExtendDeadlineRequestRequest,
) -> Response[ExtendDeadlineResponse]:
    """Extend or modify the expiration date for an assignment batch. Can reactivate expired batches by
    setting a future deadline.

    Args:
        uuid (UUID):
        body (ExtendDeadlineRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtendDeadlineResponse]
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
    body: ExtendDeadlineRequestRequest,
) -> ExtendDeadlineResponse:
    """Extend or modify the expiration date for an assignment batch. Can reactivate expired batches by
    setting a future deadline.

    Args:
        uuid (UUID):
        body (ExtendDeadlineRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtendDeadlineResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
