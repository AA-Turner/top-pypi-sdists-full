from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrow_state"] = arrow_state

    params["customer_mapping"] = customer_mapping

    json_customer_mapping_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_mapping_uuid, Unset):
        json_customer_mapping_uuid = str(customer_mapping_uuid)
    params["customer_mapping_uuid"] = json_customer_mapping_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["report_period"] = report_period

    params["report_period_from"] = report_period_from

    params["report_period_to"] = report_period_to

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["state"] = state

    params["statement_reference"] = statement_reference

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/admin/arrow/billing-syncs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            arrow_state=arrow_state,
            customer_mapping=customer_mapping,
            customer_mapping_uuid=customer_mapping_uuid,
            page=page,
            page_size=page_size,
            report_period=report_period,
            report_period_from=report_period_from,
            report_period_to=report_period_to,
            settings_uuid=settings_uuid,
            state=state,
            statement_reference=statement_reference,
        )
    ).parsed
