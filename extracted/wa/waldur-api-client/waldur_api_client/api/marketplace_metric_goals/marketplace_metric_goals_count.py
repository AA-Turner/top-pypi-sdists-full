from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_goal_period_enum import MetricGoalPeriodEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_default"] = is_default

    json_offering_metric_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_metric_uuid, Unset):
        json_offering_metric_uuid = str(offering_metric_uuid)
    params["offering_metric_uuid"] = json_offering_metric_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_period: Union[Unset, str] = UNSET
    if not isinstance(period, Unset):
        json_period = period.value

    params["period"] = json_period

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-metric-goals/",
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
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_default=is_default,
        offering_metric_uuid=offering_metric_uuid,
        page=page,
        page_size=page_size,
        period=period,
        project_uuid=project_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        is_default=is_default,
        offering_metric_uuid=offering_metric_uuid,
        page=page,
        page_size=page_size,
        period=period,
        project_uuid=project_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_default=is_default,
        offering_metric_uuid=offering_metric_uuid,
        page=page,
        page_size=page_size,
        period=period,
        project_uuid=project_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            is_default=is_default,
            offering_metric_uuid=offering_metric_uuid,
            page=page,
            page_size=page_size,
            period=period,
            project_uuid=project_uuid,
        )
    ).parsed
