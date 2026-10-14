from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_point_request import MetricPointRequest
from ...models.metric_report_result import MetricReportResult
from ...types import Response


def _get_kwargs(
    *,
    body: Union["MetricPointRequest", list["MetricPointRequest"]],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-metric-points/",
    }

    _kwargs["json"]: Union[dict[str, Any], list[dict[str, Any]]]
    if isinstance(body, MetricPointRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = []
        for componentsschemas_metric_point_report_request_type_1_item_data in body:
            componentsschemas_metric_point_report_request_type_1_item = (
                componentsschemas_metric_point_report_request_type_1_item_data.to_dict()
            )
            _kwargs["json"].append(componentsschemas_metric_point_report_request_type_1_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MetricReportResult:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MetricReportResult.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MetricReportResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["MetricPointRequest", list["MetricPointRequest"]],
) -> Response[MetricReportResult]:
    """Report metric points

     Records points for resources against metrics their offerings adopt. Send one point or a list. A
    point is identified by resource, metric, attributes and timestamp: sending it again replaces the
    value. The caller must be allowed to report usage for every resource in the request, or nothing is
    recorded (403). Other problems refuse only the affected points, listed by index.

    Args:
        body (Union['MetricPointRequest', list['MetricPointRequest']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricReportResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union["MetricPointRequest", list["MetricPointRequest"]],
) -> MetricReportResult:
    """Report metric points

     Records points for resources against metrics their offerings adopt. Send one point or a list. A
    point is identified by resource, metric, attributes and timestamp: sending it again replaces the
    value. The caller must be allowed to report usage for every resource in the request, or nothing is
    recorded (403). Other problems refuse only the affected points, listed by index.

    Args:
        body (Union['MetricPointRequest', list['MetricPointRequest']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricReportResult
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["MetricPointRequest", list["MetricPointRequest"]],
) -> Response[MetricReportResult]:
    """Report metric points

     Records points for resources against metrics their offerings adopt. Send one point or a list. A
    point is identified by resource, metric, attributes and timestamp: sending it again replaces the
    value. The caller must be allowed to report usage for every resource in the request, or nothing is
    recorded (403). Other problems refuse only the affected points, listed by index.

    Args:
        body (Union['MetricPointRequest', list['MetricPointRequest']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricReportResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union["MetricPointRequest", list["MetricPointRequest"]],
) -> MetricReportResult:
    """Report metric points

     Records points for resources against metrics their offerings adopt. Send one point or a list. A
    point is identified by resource, metric, attributes and timestamp: sending it again replaces the
    value. The caller must be allowed to report usage for every resource in the request, or nothing is
    recorded (403). Other problems refuse only the affected points, listed by index.

    Args:
        body (Union['MetricPointRequest', list['MetricPointRequest']]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricReportResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
