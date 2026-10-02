from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider_offering_user_compliance import ServiceProviderOfferingUserCompliance
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_provider_uuid: UUID,
    *,
    compliance_status: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["compliance_status"] = compliance_status

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-service-providers/{service_provider_uuid}/compliance/offering_users/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ServiceProviderOfferingUserCompliance"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ServiceProviderOfferingUserCompliance.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ServiceProviderOfferingUserCompliance"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    compliance_status: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["ServiceProviderOfferingUserCompliance"]]:
    """List offering users' compliance status

     Returns a list of offering users with their compliance status for this service provider. Can be
    filtered by offering and compliance status.

    Args:
        service_provider_uuid (UUID):
        compliance_status (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderOfferingUserCompliance']]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        compliance_status=compliance_status,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    compliance_status: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["ServiceProviderOfferingUserCompliance"]:
    """List offering users' compliance status

     Returns a list of offering users with their compliance status for this service provider. Can be
    filtered by offering and compliance status.

    Args:
        service_provider_uuid (UUID):
        compliance_status (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderOfferingUserCompliance']
    """

    return sync_detailed(
        service_provider_uuid=service_provider_uuid,
        client=client,
        compliance_status=compliance_status,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    compliance_status: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["ServiceProviderOfferingUserCompliance"]]:
    """List offering users' compliance status

     Returns a list of offering users with their compliance status for this service provider. Can be
    filtered by offering and compliance status.

    Args:
        service_provider_uuid (UUID):
        compliance_status (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderOfferingUserCompliance']]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        compliance_status=compliance_status,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    compliance_status: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["ServiceProviderOfferingUserCompliance"]:
    """List offering users' compliance status

     Returns a list of offering users with their compliance status for this service provider. Can be
    filtered by offering and compliance status.

    Args:
        service_provider_uuid (UUID):
        compliance_status (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderOfferingUserCompliance']
    """

    return (
        await asyncio_detailed(
            service_provider_uuid=service_provider_uuid,
            client=client,
            compliance_status=compliance_status,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
        )
    ).parsed
