import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_breakdown_item import MetricBreakdownItem
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_end: Union[Unset, str] = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

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
        "url": "/api/marketplace-metric-breakdown/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["MetricBreakdownItem"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MetricBreakdownItem.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MetricBreakdownItem"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> Response[list["MetricBreakdownItem"]]:
    """Break a metric figure down by an attribute or by resource

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MetricBreakdownItem']]
    """

    kwargs = _get_kwargs(
        end=end,
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
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> list["MetricBreakdownItem"]:
    """Break a metric figure down by an attribute or by resource

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricBreakdownItem']
    """

    return sync_detailed(
        client=client,
        end=end,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> Response[list["MetricBreakdownItem"]]:
    """Break a metric figure down by an attribute or by resource

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MetricBreakdownItem']]
    """

    kwargs = _get_kwargs(
        end=end,
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
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> list["MetricBreakdownItem"]:
    """Break a metric figure down by an attribute or by resource

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricBreakdownItem']
    """

    return (
        await asyncio_detailed(
            client=client,
            end=end,
            group_by=group_by,
            offering_metric_uuid=offering_metric_uuid,
            project_uuid=project_uuid,
            resource_uuid=resource_uuid,
            start=start,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> list["MetricBreakdownItem"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricBreakdownItem']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricBreakdownItem] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        end=end,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
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
    end: Union[Unset, datetime.datetime] = UNSET,
    group_by: str,
    offering_metric_uuid: UUID,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start: datetime.datetime,
) -> list["MetricBreakdownItem"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        end (Union[Unset, datetime.datetime]):
        group_by (str):
        offering_metric_uuid (UUID):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricBreakdownItem']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricBreakdownItem] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        end=end,
        group_by=group_by,
        offering_metric_uuid=offering_metric_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start=start,
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
