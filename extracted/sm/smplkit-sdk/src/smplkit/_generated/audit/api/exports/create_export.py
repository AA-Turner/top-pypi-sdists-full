from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.export_request import ExportRequest
from ...models.export_response import ExportResponse


def _get_kwargs(
    *,
    body: ExportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/exports",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ExportResponse | None:
    if response.status_code == 201:
        response_201 = ExportResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ExportResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ExportRequest,
) -> Response[ExportResponse]:
    """Create Export

     Mint a short-lived signed URL to stream an events download.

    The request body specifies `format` (`CSV` or `JSONL`) and any
    subset of the event filters accepted by `GET /api/v1/events`. An
    export is scoped to a single environment: name it in the body's
    `environment` field, or omit it and a single-environment credential
    implies it (a multi-environment credential must name it). The
    response returns the signed URL plus its expiry (30 seconds from
    mint). Open the URL in a browser to stream the file to disk; no
    `Authorization` header is required at download time.

    Filter rules match `GET /api/v1/events`: `filter[resource_id]`
    requires `filter[resource_type]`; `filter[search]` requires either
    `filter[occurred_at]` or `filter[resource_type]` +
    `filter[resource_id]`. Violations are rejected here at mint time.

    Reads are allowed on lapsed subscriptions per the smplcore
    convention — same gate as the events list.

    Args:
        body (ExportRequest): JSON:API request envelope for minting a signed download URL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportResponse]
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
    body: ExportRequest,
) -> ExportResponse | None:
    """Create Export

     Mint a short-lived signed URL to stream an events download.

    The request body specifies `format` (`CSV` or `JSONL`) and any
    subset of the event filters accepted by `GET /api/v1/events`. An
    export is scoped to a single environment: name it in the body's
    `environment` field, or omit it and a single-environment credential
    implies it (a multi-environment credential must name it). The
    response returns the signed URL plus its expiry (30 seconds from
    mint). Open the URL in a browser to stream the file to disk; no
    `Authorization` header is required at download time.

    Filter rules match `GET /api/v1/events`: `filter[resource_id]`
    requires `filter[resource_type]`; `filter[search]` requires either
    `filter[occurred_at]` or `filter[resource_type]` +
    `filter[resource_id]`. Violations are rejected here at mint time.

    Reads are allowed on lapsed subscriptions per the smplcore
    convention — same gate as the events list.

    Args:
        body (ExportRequest): JSON:API request envelope for minting a signed download URL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ExportRequest,
) -> Response[ExportResponse]:
    """Create Export

     Mint a short-lived signed URL to stream an events download.

    The request body specifies `format` (`CSV` or `JSONL`) and any
    subset of the event filters accepted by `GET /api/v1/events`. An
    export is scoped to a single environment: name it in the body's
    `environment` field, or omit it and a single-environment credential
    implies it (a multi-environment credential must name it). The
    response returns the signed URL plus its expiry (30 seconds from
    mint). Open the URL in a browser to stream the file to disk; no
    `Authorization` header is required at download time.

    Filter rules match `GET /api/v1/events`: `filter[resource_id]`
    requires `filter[resource_type]`; `filter[search]` requires either
    `filter[occurred_at]` or `filter[resource_type]` +
    `filter[resource_id]`. Violations are rejected here at mint time.

    Reads are allowed on lapsed subscriptions per the smplcore
    convention — same gate as the events list.

    Args:
        body (ExportRequest): JSON:API request envelope for minting a signed download URL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ExportRequest,
) -> ExportResponse | None:
    """Create Export

     Mint a short-lived signed URL to stream an events download.

    The request body specifies `format` (`CSV` or `JSONL`) and any
    subset of the event filters accepted by `GET /api/v1/events`. An
    export is scoped to a single environment: name it in the body's
    `environment` field, or omit it and a single-environment credential
    implies it (a multi-environment credential must name it). The
    response returns the signed URL plus its expiry (30 seconds from
    mint). Open the URL in a browser to stream the file to disk; no
    `Authorization` header is required at download time.

    Filter rules match `GET /api/v1/events`: `filter[resource_id]`
    requires `filter[resource_type]`; `filter[search]` requires either
    `filter[occurred_at]` or `filter[resource_type]` +
    `filter[resource_id]`. Violations are rejected here at mint time.

    Reads are allowed on lapsed subscriptions per the smplcore
    convention — same gate as the events list.

    Args:
        body (ExportRequest): JSON:API request envelope for minting a signed download URL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
