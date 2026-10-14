from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_goal import MetricGoal
from ...models.metric_goal_period_enum import MetricGoalPeriodEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/marketplace-metric-goals/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["MetricGoal"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MetricGoal.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MetricGoal"]]:
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
) -> Response[list["MetricGoal"]]:
    """
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
        Response[list['MetricGoal']]
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
) -> list["MetricGoal"]:
    """
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
        list['MetricGoal']
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
) -> Response[list["MetricGoal"]]:
    """
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
        Response[list['MetricGoal']]
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
) -> list["MetricGoal"]:
    """
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
        list['MetricGoal']
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


def sync_all(
    *,
    client: AuthenticatedClient,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> list["MetricGoal"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricGoal']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricGoal] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_default=is_default,
        offering_metric_uuid=offering_metric_uuid,
        period=period,
        project_uuid=project_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    is_default: Union[Unset, bool] = UNSET,
    offering_metric_uuid: Union[Unset, UUID] = UNSET,
    period: Union[Unset, MetricGoalPeriodEnum] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
) -> list["MetricGoal"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_default (Union[Unset, bool]):
        offering_metric_uuid (Union[Unset, UUID]):
        period (Union[Unset, MetricGoalPeriodEnum]):
        project_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricGoal']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricGoal] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_default=is_default,
        offering_metric_uuid=offering_metric_uuid,
        period=period,
        project_uuid=project_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
