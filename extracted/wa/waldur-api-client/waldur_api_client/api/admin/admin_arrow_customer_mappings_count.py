from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrow_company_name"] = arrow_company_name

    params["arrow_reference"] = arrow_reference

    params["is_active"] = is_active

    params["page"] = page

    params["page_size"] = page_size

    params["settings"] = settings

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["waldur_customer"] = waldur_customer

    json_waldur_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(waldur_customer_uuid, Unset):
        json_waldur_customer_uuid = str(waldur_customer_uuid)
    params["waldur_customer_uuid"] = json_waldur_customer_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/admin/arrow/customer-mappings/",
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
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            arrow_company_name=arrow_company_name,
            arrow_reference=arrow_reference,
            is_active=is_active,
            page=page,
            page_size=page_size,
            settings=settings,
            settings_uuid=settings_uuid,
            waldur_customer=waldur_customer,
            waldur_customer_uuid=waldur_customer_uuid,
        )
    ).parsed
