from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_usage_by_project import OfferingUsageByProject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    component_type: Union[Unset, str] = UNSET,
    offering_uuid: UUID,
    period_offset: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["component_type"] = component_type

    json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["period_offset"] = period_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-customer-usage/{uuid}/components-usage-by-project/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OfferingUsageByProject:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingUsageByProject.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingUsageByProject]:
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
    component_type: Union[Unset, str] = UNSET,
    offering_uuid: UUID,
    period_offset: Union[Unset, int] = UNSET,
) -> Response[OfferingUsageByProject]:
    """Get per-project usage breakdown for a single offering

     Returns the customer's usage of one offering broken down by project. Each project entry includes an
    in-period total `usage` and a monthly `buckets` array. Projects are sorted by usage descending.

    Args:
        uuid (UUID):
        component_type (Union[Unset, str]):
        offering_uuid (UUID):
        period_offset (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUsageByProject]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        component_type=component_type,
        offering_uuid=offering_uuid,
        period_offset=period_offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    component_type: Union[Unset, str] = UNSET,
    offering_uuid: UUID,
    period_offset: Union[Unset, int] = UNSET,
) -> OfferingUsageByProject:
    """Get per-project usage breakdown for a single offering

     Returns the customer's usage of one offering broken down by project. Each project entry includes an
    in-period total `usage` and a monthly `buckets` array. Projects are sorted by usage descending.

    Args:
        uuid (UUID):
        component_type (Union[Unset, str]):
        offering_uuid (UUID):
        period_offset (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUsageByProject
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        component_type=component_type,
        offering_uuid=offering_uuid,
        period_offset=period_offset,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    component_type: Union[Unset, str] = UNSET,
    offering_uuid: UUID,
    period_offset: Union[Unset, int] = UNSET,
) -> Response[OfferingUsageByProject]:
    """Get per-project usage breakdown for a single offering

     Returns the customer's usage of one offering broken down by project. Each project entry includes an
    in-period total `usage` and a monthly `buckets` array. Projects are sorted by usage descending.

    Args:
        uuid (UUID):
        component_type (Union[Unset, str]):
        offering_uuid (UUID):
        period_offset (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUsageByProject]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        component_type=component_type,
        offering_uuid=offering_uuid,
        period_offset=period_offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    component_type: Union[Unset, str] = UNSET,
    offering_uuid: UUID,
    period_offset: Union[Unset, int] = UNSET,
) -> OfferingUsageByProject:
    """Get per-project usage breakdown for a single offering

     Returns the customer's usage of one offering broken down by project. Each project entry includes an
    in-period total `usage` and a monthly `buckets` array. Projects are sorted by usage descending.

    Args:
        uuid (UUID):
        component_type (Union[Unset, str]):
        offering_uuid (UUID):
        period_offset (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUsageByProject
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            component_type=component_type,
            offering_uuid=offering_uuid,
            period_offset=period_offset,
        )
    ).parsed
