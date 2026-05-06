from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_kpi_response import AnonymousChatKpiResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/anonymous-chat-interactions/kpi/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> AnonymousChatKpiResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AnonymousChatKpiResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnonymousChatKpiResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AnonymousChatKpiResponse]:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatKpiResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> AnonymousChatKpiResponse:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatKpiResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AnonymousChatKpiResponse]:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatKpiResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> AnonymousChatKpiResponse:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatKpiResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
