import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_user_usage_o_enum import ComponentUserUsageOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    billing_period_month: Union[Unset, float] = UNSET,
    billing_period_year: Union[Unset, float] = UNSET,
    component_usage_billing_period: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ComponentUserUsageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    type_: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["billing_period_month"] = billing_period_month

    params["billing_period_year"] = billing_period_year

    json_component_usage_billing_period: Union[Unset, str] = UNSET
    if not isinstance(component_usage_billing_period, Unset):
        json_component_usage_billing_period = component_usage_billing_period.isoformat()
    params["component_usage__billing_period"] = json_component_usage_billing_period

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_date_after: Union[Unset, str] = UNSET
    if not isinstance(date_after, Unset):
        json_date_after = date_after.isoformat()
    params["date_after"] = json_date_after

    json_date_before: Union[Unset, str] = UNSET
    if not isinstance(date_before, Unset):
        json_date_before = date_before.isoformat()
    params["date_before"] = json_date_before

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

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["resource"] = resource

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    params["type"] = type_

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-component-user-usages/",
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
    billing_period_month: Union[Unset, float] = UNSET,
    billing_period_year: Union[Unset, float] = UNSET,
    component_usage_billing_period: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ComponentUserUsageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    type_: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List user-specific component usages

     Get number of items in the collection matching the request parameters.

    Args:
        billing_period_month (Union[Unset, float]):
        billing_period_year (Union[Unset, float]):
        component_usage_billing_period (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ComponentUserUsageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        type_ (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        billing_period_month=billing_period_month,
        billing_period_year=billing_period_year,
        component_usage_billing_period=component_usage_billing_period,
        customer_uuid=customer_uuid,
        date_after=date_after,
        date_before=date_before,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        type_=type_,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    billing_period_month: Union[Unset, float] = UNSET,
    billing_period_year: Union[Unset, float] = UNSET,
    component_usage_billing_period: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ComponentUserUsageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    type_: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List user-specific component usages

     Get number of items in the collection matching the request parameters.

    Args:
        billing_period_month (Union[Unset, float]):
        billing_period_year (Union[Unset, float]):
        component_usage_billing_period (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ComponentUserUsageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        type_ (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        billing_period_month=billing_period_month,
        billing_period_year=billing_period_year,
        component_usage_billing_period=component_usage_billing_period,
        customer_uuid=customer_uuid,
        date_after=date_after,
        date_before=date_before,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        type_=type_,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    billing_period_month: Union[Unset, float] = UNSET,
    billing_period_year: Union[Unset, float] = UNSET,
    component_usage_billing_period: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ComponentUserUsageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    type_: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List user-specific component usages

     Get number of items in the collection matching the request parameters.

    Args:
        billing_period_month (Union[Unset, float]):
        billing_period_year (Union[Unset, float]):
        component_usage_billing_period (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ComponentUserUsageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        type_ (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        billing_period_month=billing_period_month,
        billing_period_year=billing_period_year,
        component_usage_billing_period=component_usage_billing_period,
        customer_uuid=customer_uuid,
        date_after=date_after,
        date_before=date_before,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        resource=resource,
        resource_uuid=resource_uuid,
        type_=type_,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    billing_period_month: Union[Unset, float] = UNSET,
    billing_period_year: Union[Unset, float] = UNSET,
    component_usage_billing_period: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ComponentUserUsageOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    type_: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List user-specific component usages

     Get number of items in the collection matching the request parameters.

    Args:
        billing_period_month (Union[Unset, float]):
        billing_period_year (Union[Unset, float]):
        component_usage_billing_period (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ComponentUserUsageOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        type_ (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            billing_period_month=billing_period_month,
            billing_period_year=billing_period_year,
            component_usage_billing_period=component_usage_billing_period,
            customer_uuid=customer_uuid,
            date_after=date_after,
            date_before=date_before,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            resource=resource,
            resource_uuid=resource_uuid,
            type_=type_,
            username=username,
        )
    ).parsed
