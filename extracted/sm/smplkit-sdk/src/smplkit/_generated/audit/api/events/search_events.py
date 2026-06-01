from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.event_search_request import EventSearchRequest
from ...models.event_search_response import EventSearchResponse


def _get_kwargs(
    *,
    body: EventSearchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/events/search",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EventSearchResponse | None:
    if response.status_code == 200:
        response_200 = EventSearchResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[EventSearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: EventSearchRequest,
) -> Response[EventSearchResponse]:
    r"""Search Events

     Search audit events with column filters and an optional JSON Logic expression.

    Without a JSON Logic `filter`: behaves like `GET /api/v1/events`
    with the same column filters.

    With a JSON Logic `filter`: the search is silently capped to the
    last 30 days by `occurred_at` (intersected with any explicit
    `filter[occurred_at]` the caller supplied), the column filters
    narrow the candidate set in SQL, and the JSON Logic expression
    runs in memory against each candidate row using the same
    `json-logic-qubit` evaluator the forwarder pipeline uses. Up to
    50,000 rows are scanned per request; the response's `meta.scan`
    block reports the scan stats so a selective filter doesn't look
    like \"0 matches\" when the truth is \"ceiling reached.\"

    Args:
        body (EventSearchRequest): Request body for ``POST /api/v1/events/search``.

            Mirrors every column filter accepted by ``GET /api/v1/events`` with
            identical semantics, and adds a top-level ``filter`` field carrying
            a JSON Logic expression. When ``filter`` is present the search is
            silently capped to the last 30 days by ``occurred_at``; the
            expression is then evaluated in memory against each row that passes
            the column filters using the same ``json-logic-qubit`` evaluator
            that runs in the forwarder pipeline (so search results match what
            would be forwarded).

            Filter-combination rules match ``GET /api/v1/events`` exactly:

            - ``filter[resource_id]`` must be accompanied by
              ``filter[resource_type]`` — the index is keyed on the pair.
            - ``filter[search]`` must be accompanied by either
              ``filter[occurred_at]`` or ``filter[resource_type]`` +
              ``filter[resource_id]`` — substring matching has no index, so an
              unbounded substring scan is rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventSearchResponse]
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
    body: EventSearchRequest,
) -> EventSearchResponse | None:
    r"""Search Events

     Search audit events with column filters and an optional JSON Logic expression.

    Without a JSON Logic `filter`: behaves like `GET /api/v1/events`
    with the same column filters.

    With a JSON Logic `filter`: the search is silently capped to the
    last 30 days by `occurred_at` (intersected with any explicit
    `filter[occurred_at]` the caller supplied), the column filters
    narrow the candidate set in SQL, and the JSON Logic expression
    runs in memory against each candidate row using the same
    `json-logic-qubit` evaluator the forwarder pipeline uses. Up to
    50,000 rows are scanned per request; the response's `meta.scan`
    block reports the scan stats so a selective filter doesn't look
    like \"0 matches\" when the truth is \"ceiling reached.\"

    Args:
        body (EventSearchRequest): Request body for ``POST /api/v1/events/search``.

            Mirrors every column filter accepted by ``GET /api/v1/events`` with
            identical semantics, and adds a top-level ``filter`` field carrying
            a JSON Logic expression. When ``filter`` is present the search is
            silently capped to the last 30 days by ``occurred_at``; the
            expression is then evaluated in memory against each row that passes
            the column filters using the same ``json-logic-qubit`` evaluator
            that runs in the forwarder pipeline (so search results match what
            would be forwarded).

            Filter-combination rules match ``GET /api/v1/events`` exactly:

            - ``filter[resource_id]`` must be accompanied by
              ``filter[resource_type]`` — the index is keyed on the pair.
            - ``filter[search]`` must be accompanied by either
              ``filter[occurred_at]`` or ``filter[resource_type]`` +
              ``filter[resource_id]`` — substring matching has no index, so an
              unbounded substring scan is rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventSearchResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: EventSearchRequest,
) -> Response[EventSearchResponse]:
    r"""Search Events

     Search audit events with column filters and an optional JSON Logic expression.

    Without a JSON Logic `filter`: behaves like `GET /api/v1/events`
    with the same column filters.

    With a JSON Logic `filter`: the search is silently capped to the
    last 30 days by `occurred_at` (intersected with any explicit
    `filter[occurred_at]` the caller supplied), the column filters
    narrow the candidate set in SQL, and the JSON Logic expression
    runs in memory against each candidate row using the same
    `json-logic-qubit` evaluator the forwarder pipeline uses. Up to
    50,000 rows are scanned per request; the response's `meta.scan`
    block reports the scan stats so a selective filter doesn't look
    like \"0 matches\" when the truth is \"ceiling reached.\"

    Args:
        body (EventSearchRequest): Request body for ``POST /api/v1/events/search``.

            Mirrors every column filter accepted by ``GET /api/v1/events`` with
            identical semantics, and adds a top-level ``filter`` field carrying
            a JSON Logic expression. When ``filter`` is present the search is
            silently capped to the last 30 days by ``occurred_at``; the
            expression is then evaluated in memory against each row that passes
            the column filters using the same ``json-logic-qubit`` evaluator
            that runs in the forwarder pipeline (so search results match what
            would be forwarded).

            Filter-combination rules match ``GET /api/v1/events`` exactly:

            - ``filter[resource_id]`` must be accompanied by
              ``filter[resource_type]`` — the index is keyed on the pair.
            - ``filter[search]`` must be accompanied by either
              ``filter[occurred_at]`` or ``filter[resource_type]`` +
              ``filter[resource_id]`` — substring matching has no index, so an
              unbounded substring scan is rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventSearchResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: EventSearchRequest,
) -> EventSearchResponse | None:
    r"""Search Events

     Search audit events with column filters and an optional JSON Logic expression.

    Without a JSON Logic `filter`: behaves like `GET /api/v1/events`
    with the same column filters.

    With a JSON Logic `filter`: the search is silently capped to the
    last 30 days by `occurred_at` (intersected with any explicit
    `filter[occurred_at]` the caller supplied), the column filters
    narrow the candidate set in SQL, and the JSON Logic expression
    runs in memory against each candidate row using the same
    `json-logic-qubit` evaluator the forwarder pipeline uses. Up to
    50,000 rows are scanned per request; the response's `meta.scan`
    block reports the scan stats so a selective filter doesn't look
    like \"0 matches\" when the truth is \"ceiling reached.\"

    Args:
        body (EventSearchRequest): Request body for ``POST /api/v1/events/search``.

            Mirrors every column filter accepted by ``GET /api/v1/events`` with
            identical semantics, and adds a top-level ``filter`` field carrying
            a JSON Logic expression. When ``filter`` is present the search is
            silently capped to the last 30 days by ``occurred_at``; the
            expression is then evaluated in memory against each row that passes
            the column filters using the same ``json-logic-qubit`` evaluator
            that runs in the forwarder pipeline (so search results match what
            would be forwarded).

            Filter-combination rules match ``GET /api/v1/events`` exactly:

            - ``filter[resource_id]`` must be accompanied by
              ``filter[resource_type]`` — the index is keyed on the pair.
            - ``filter[search]`` must be accompanied by either
              ``filter[occurred_at]`` or ``filter[resource_type]`` +
              ``filter[resource_id]`` — substring matching has no index, so an
              unbounded substring scan is rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventSearchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
