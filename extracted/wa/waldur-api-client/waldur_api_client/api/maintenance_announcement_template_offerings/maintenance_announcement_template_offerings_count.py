from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_req_o_enum import BackendResourceReqOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    impact_level: Union[Unset, int] = UNSET,
    maintenance_template_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["impact_level"] = impact_level

    json_maintenance_template_uuid: Union[Unset, str] = UNSET
    if not isinstance(maintenance_template_uuid, Unset):
        json_maintenance_template_uuid = str(maintenance_template_uuid)
    params["maintenance_template_uuid"] = json_maintenance_template_uuid

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_service_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_provider_uuid, Unset):
        json_service_provider_uuid = str(service_provider_uuid)
    params["service_provider_uuid"] = json_service_provider_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/maintenance-announcement-template-offerings/",
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
    impact_level: Union[Unset, int] = UNSET,
    maintenance_template_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List affected offering templates

     Get number of items in the collection matching the request parameters.

    Args:
        impact_level (Union[Unset, int]):
        maintenance_template_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        impact_level=impact_level,
        maintenance_template_uuid=maintenance_template_uuid,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    impact_level: Union[Unset, int] = UNSET,
    maintenance_template_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List affected offering templates

     Get number of items in the collection matching the request parameters.

    Args:
        impact_level (Union[Unset, int]):
        maintenance_template_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        impact_level=impact_level,
        maintenance_template_uuid=maintenance_template_uuid,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    impact_level: Union[Unset, int] = UNSET,
    maintenance_template_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List affected offering templates

     Get number of items in the collection matching the request parameters.

    Args:
        impact_level (Union[Unset, int]):
        maintenance_template_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        impact_level=impact_level,
        maintenance_template_uuid=maintenance_template_uuid,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    impact_level: Union[Unset, int] = UNSET,
    maintenance_template_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[BackendResourceReqOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List affected offering templates

     Get number of items in the collection matching the request parameters.

    Args:
        impact_level (Union[Unset, int]):
        maintenance_template_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[BackendResourceReqOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            impact_level=impact_level,
            maintenance_template_uuid=maintenance_template_uuid,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            service_provider_uuid=service_provider_uuid,
        )
    ).parsed
