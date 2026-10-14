import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_series_response import MetricSeriesResponse
from ...models.metric_series_response_aggregate_enum import MetricSeriesResponseAggregateEnum
from ...models.metric_series_response_granularity_enum import MetricSeriesResponseGranularityEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    aggregate: Union[Unset, MetricSeriesResponseAggregateEnum] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    granularity: Union[Unset, MetricSeriesResponseGranularityEnum] = UNSET,
    group_by: Union[Unset, str] = UNSET,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_aggregate: Union[Unset, str] = UNSET
    if not isinstance(aggregate, Unset):
        json_aggregate = aggregate.value

    params["aggregate"] = json_aggregate

    json_end: Union[Unset, str] = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

    json_granularity: Union[Unset, str] = UNSET
    if not isinstance(granularity, Unset):
        json_granularity = granularity.value

    params["granularity"] = json_granularity

    params["group_by"] = group_by

    json_offering_metric_uuid = str(offering_metric_uuid)
    params["offering_metric_uuid"] = json_offering_metric_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_start = start.isoformat()
    params["start"] = json_start

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-metric-series/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MetricSeriesResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MetricSeriesResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MetricSeriesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    aggregate: Union[Unset, MetricSeriesResponseAggregateEnum] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    granularity: Union[Unset, MetricSeriesResponseGranularityEnum] = UNSET,
    group_by: Union[Unset, str] = UNSET,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> Response[MetricSeriesResponse]:
    """Get metric series

    Args:
        aggregate (Union[Unset, MetricSeriesResponseAggregateEnum]):
        end (Union[Unset, datetime.datetime]):
        granularity (Union[Unset, MetricSeriesResponseGranularityEnum]):
        group_by (Union[Unset, str]):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricSeriesResponse]
    """

    kwargs = _get_kwargs(
        aggregate=aggregate,
        end=end,
        granularity=granularity,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    aggregate: Union[Unset, MetricSeriesResponseAggregateEnum] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    granularity: Union[Unset, MetricSeriesResponseGranularityEnum] = UNSET,
    group_by: Union[Unset, str] = UNSET,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> MetricSeriesResponse:
    """Get metric series

    Args:
        aggregate (Union[Unset, MetricSeriesResponseAggregateEnum]):
        end (Union[Unset, datetime.datetime]):
        granularity (Union[Unset, MetricSeriesResponseGranularityEnum]):
        group_by (Union[Unset, str]):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricSeriesResponse
    """

    return sync_detailed(
        client=client,
        aggregate=aggregate,
        end=end,
        granularity=granularity,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    aggregate: Union[Unset, MetricSeriesResponseAggregateEnum] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    granularity: Union[Unset, MetricSeriesResponseGranularityEnum] = UNSET,
    group_by: Union[Unset, str] = UNSET,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> Response[MetricSeriesResponse]:
    """Get metric series

    Args:
        aggregate (Union[Unset, MetricSeriesResponseAggregateEnum]):
        end (Union[Unset, datetime.datetime]):
        granularity (Union[Unset, MetricSeriesResponseGranularityEnum]):
        group_by (Union[Unset, str]):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricSeriesResponse]
    """

    kwargs = _get_kwargs(
        aggregate=aggregate,
        end=end,
        granularity=granularity,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    aggregate: Union[Unset, MetricSeriesResponseAggregateEnum] = UNSET,
    end: Union[Unset, datetime.datetime] = UNSET,
    granularity: Union[Unset, MetricSeriesResponseGranularityEnum] = UNSET,
    group_by: Union[Unset, str] = UNSET,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> MetricSeriesResponse:
    """Get metric series

    Args:
        aggregate (Union[Unset, MetricSeriesResponseAggregateEnum]):
        end (Union[Unset, datetime.datetime]):
        granularity (Union[Unset, MetricSeriesResponseGranularityEnum]):
        group_by (Union[Unset, str]):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricSeriesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            aggregate=aggregate,
            end=end,
            granularity=granularity,
            group_by=group_by,
            offering_metric_uuid=offering_metric_uuid,
            project_uuid=project_uuid,
            resource_uuid=resource_uuid,
            start=start,
        )
    ).parsed
