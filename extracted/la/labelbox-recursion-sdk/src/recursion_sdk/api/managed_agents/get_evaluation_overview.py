from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_evaluation_overview_range import GetEvaluationOverviewRange
from ...models.get_evaluation_overview_series_metric import GetEvaluationOverviewSeriesMetric
from ...models.get_evaluation_overview_series_resolution import GetEvaluationOverviewSeriesResolution
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_evaluation_overview_response import ManagedAgentsEvaluationOverviewResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    range_: GetEvaluationOverviewRange | Unset = GetEvaluationOverviewRange.VALUE_1,
    evaluator_agent_version_id: UUID,
    target_agent_id: UUID | Unset = UNSET,
    series_target_agent_id: list[UUID] | Unset = UNSET,
    series_previous_target_agent_version_id: list[UUID] | Unset = UNSET,
    series_metric: GetEvaluationOverviewSeriesMetric | Unset = GetEvaluationOverviewSeriesMetric.OVERALL,
    series_criterion_key: str | Unset = UNSET,
    series_resolution: GetEvaluationOverviewSeriesResolution | Unset = UNSET,
    limit: int | Unset = 25,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_range_: str | Unset = UNSET
    if not isinstance(range_, Unset):
        json_range_ = range_.value

    params["range"] = json_range_

    json_evaluator_agent_version_id = str(evaluator_agent_version_id)
    params["evaluator_agent_version_id"] = json_evaluator_agent_version_id

    json_target_agent_id: str | Unset = UNSET
    if not isinstance(target_agent_id, Unset):
        json_target_agent_id = str(target_agent_id)
    params["target_agent_id"] = json_target_agent_id

    json_series_target_agent_id: list[str] | Unset = UNSET
    if not isinstance(series_target_agent_id, Unset):
        json_series_target_agent_id = []
        for series_target_agent_id_item_data in series_target_agent_id:
            series_target_agent_id_item = str(series_target_agent_id_item_data)
            json_series_target_agent_id.append(series_target_agent_id_item)


    params["series_target_agent_id"] = json_series_target_agent_id

    json_series_previous_target_agent_version_id: list[str] | Unset = UNSET
    if not isinstance(series_previous_target_agent_version_id, Unset):
        json_series_previous_target_agent_version_id = []
        for series_previous_target_agent_version_id_item_data in series_previous_target_agent_version_id:
            series_previous_target_agent_version_id_item = str(series_previous_target_agent_version_id_item_data)
            json_series_previous_target_agent_version_id.append(series_previous_target_agent_version_id_item)


    params["series_previous_target_agent_version_id"] = json_series_previous_target_agent_version_id

    json_series_metric: str | Unset = UNSET
    if not isinstance(series_metric, Unset):
        json_series_metric = series_metric.value

    params["series_metric"] = json_series_metric

    params["series_criterion_key"] = series_criterion_key

    json_series_resolution: str | Unset = UNSET
    if not isinstance(series_resolution, Unset):
        json_series_resolution = series_resolution.value

    params["series_resolution"] = json_series_resolution

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/evaluations/overview",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEvaluationOverviewResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    range_: GetEvaluationOverviewRange | Unset = GetEvaluationOverviewRange.VALUE_1,
    evaluator_agent_version_id: UUID,
    target_agent_id: UUID | Unset = UNSET,
    series_target_agent_id: list[UUID] | Unset = UNSET,
    series_previous_target_agent_version_id: list[UUID] | Unset = UNSET,
    series_metric: GetEvaluationOverviewSeriesMetric | Unset = GetEvaluationOverviewSeriesMetric.OVERALL,
    series_criterion_key: str | Unset = UNSET,
    series_resolution: GetEvaluationOverviewSeriesResolution | Unset = UNSET,
    limit: int | Unset = 25,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse]:
    """ Get evaluation overview

     Returns one server-composed evaluation dashboard page from a fixed batch of strong-snapshot reads at
    the durable analytics watermark. Current and prior windows are adjacent and equal; cohort history
    gaps produce explicit null coverage fields rather than misleading zeroes.

    Args:
        range_ (GetEvaluationOverviewRange | Unset): Length of the current window. The prior
            window is the adjacent interval of equal length. Default:
            GetEvaluationOverviewRange.VALUE_1.
        evaluator_agent_version_id (UUID): Immutable evaluation-agent version whose rubric and
            verdicts define this overview.
        target_agent_id (UUID | Unset): Optionally narrow page-level metrics, table rows, and
            retained history to one target agent.
        series_target_agent_id (list[UUID] | Unset): Repeat to explicitly compare up to five
            target agents; absent values select the page target or the first five whole-filter agents.
        series_previous_target_agent_version_id (list[UUID] | Unset): Repeat to add scoped
            previous target-agent versions; automatic latest versions plus these values may total at
            most twelve traces.
        series_metric (GetEvaluationOverviewSeriesMetric | Unset): Verdict population plotted for
            each selected target-agent version. Default: GetEvaluationOverviewSeriesMetric.OVERALL.
        series_criterion_key (str | Unset): Rubric key plotted when series_metric is criterion;
            required exactly for that metric.
        series_resolution (GetEvaluationOverviewSeriesResolution | Unset): Opt into bounded
            adaptive chart positions from exact timestamps through days. Omit for the legacy fixed
            daily grid.
        limit (int | Unset): Maximum target-agent rows to return. Defaults to 25. Default: 25.
        page_token (str | Unset): Opaque signed continuation bound to the organization, frozen
            watermark, range, evaluator, singular table target, and effective limit. Comparison
            agents, versions, and metric may change without resetting the table page. Expires after
            one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse]
     """


    kwargs = _get_kwargs(
        range_=range_,
evaluator_agent_version_id=evaluator_agent_version_id,
target_agent_id=target_agent_id,
series_target_agent_id=series_target_agent_id,
series_previous_target_agent_version_id=series_previous_target_agent_version_id,
series_metric=series_metric,
series_criterion_key=series_criterion_key,
series_resolution=series_resolution,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    range_: GetEvaluationOverviewRange | Unset = GetEvaluationOverviewRange.VALUE_1,
    evaluator_agent_version_id: UUID,
    target_agent_id: UUID | Unset = UNSET,
    series_target_agent_id: list[UUID] | Unset = UNSET,
    series_previous_target_agent_version_id: list[UUID] | Unset = UNSET,
    series_metric: GetEvaluationOverviewSeriesMetric | Unset = GetEvaluationOverviewSeriesMetric.OVERALL,
    series_criterion_key: str | Unset = UNSET,
    series_resolution: GetEvaluationOverviewSeriesResolution | Unset = UNSET,
    limit: int | Unset = 25,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse | None:
    """ Get evaluation overview

     Returns one server-composed evaluation dashboard page from a fixed batch of strong-snapshot reads at
    the durable analytics watermark. Current and prior windows are adjacent and equal; cohort history
    gaps produce explicit null coverage fields rather than misleading zeroes.

    Args:
        range_ (GetEvaluationOverviewRange | Unset): Length of the current window. The prior
            window is the adjacent interval of equal length. Default:
            GetEvaluationOverviewRange.VALUE_1.
        evaluator_agent_version_id (UUID): Immutable evaluation-agent version whose rubric and
            verdicts define this overview.
        target_agent_id (UUID | Unset): Optionally narrow page-level metrics, table rows, and
            retained history to one target agent.
        series_target_agent_id (list[UUID] | Unset): Repeat to explicitly compare up to five
            target agents; absent values select the page target or the first five whole-filter agents.
        series_previous_target_agent_version_id (list[UUID] | Unset): Repeat to add scoped
            previous target-agent versions; automatic latest versions plus these values may total at
            most twelve traces.
        series_metric (GetEvaluationOverviewSeriesMetric | Unset): Verdict population plotted for
            each selected target-agent version. Default: GetEvaluationOverviewSeriesMetric.OVERALL.
        series_criterion_key (str | Unset): Rubric key plotted when series_metric is criterion;
            required exactly for that metric.
        series_resolution (GetEvaluationOverviewSeriesResolution | Unset): Opt into bounded
            adaptive chart positions from exact timestamps through days. Omit for the legacy fixed
            daily grid.
        limit (int | Unset): Maximum target-agent rows to return. Defaults to 25. Default: 25.
        page_token (str | Unset): Opaque signed continuation bound to the organization, frozen
            watermark, range, evaluator, singular table target, and effective limit. Comparison
            agents, versions, and metric may change without resetting the table page. Expires after
            one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse
     """


    return sync_detailed(
        client=client,
range_=range_,
evaluator_agent_version_id=evaluator_agent_version_id,
target_agent_id=target_agent_id,
series_target_agent_id=series_target_agent_id,
series_previous_target_agent_version_id=series_previous_target_agent_version_id,
series_metric=series_metric,
series_criterion_key=series_criterion_key,
series_resolution=series_resolution,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    range_: GetEvaluationOverviewRange | Unset = GetEvaluationOverviewRange.VALUE_1,
    evaluator_agent_version_id: UUID,
    target_agent_id: UUID | Unset = UNSET,
    series_target_agent_id: list[UUID] | Unset = UNSET,
    series_previous_target_agent_version_id: list[UUID] | Unset = UNSET,
    series_metric: GetEvaluationOverviewSeriesMetric | Unset = GetEvaluationOverviewSeriesMetric.OVERALL,
    series_criterion_key: str | Unset = UNSET,
    series_resolution: GetEvaluationOverviewSeriesResolution | Unset = UNSET,
    limit: int | Unset = 25,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse]:
    """ Get evaluation overview

     Returns one server-composed evaluation dashboard page from a fixed batch of strong-snapshot reads at
    the durable analytics watermark. Current and prior windows are adjacent and equal; cohort history
    gaps produce explicit null coverage fields rather than misleading zeroes.

    Args:
        range_ (GetEvaluationOverviewRange | Unset): Length of the current window. The prior
            window is the adjacent interval of equal length. Default:
            GetEvaluationOverviewRange.VALUE_1.
        evaluator_agent_version_id (UUID): Immutable evaluation-agent version whose rubric and
            verdicts define this overview.
        target_agent_id (UUID | Unset): Optionally narrow page-level metrics, table rows, and
            retained history to one target agent.
        series_target_agent_id (list[UUID] | Unset): Repeat to explicitly compare up to five
            target agents; absent values select the page target or the first five whole-filter agents.
        series_previous_target_agent_version_id (list[UUID] | Unset): Repeat to add scoped
            previous target-agent versions; automatic latest versions plus these values may total at
            most twelve traces.
        series_metric (GetEvaluationOverviewSeriesMetric | Unset): Verdict population plotted for
            each selected target-agent version. Default: GetEvaluationOverviewSeriesMetric.OVERALL.
        series_criterion_key (str | Unset): Rubric key plotted when series_metric is criterion;
            required exactly for that metric.
        series_resolution (GetEvaluationOverviewSeriesResolution | Unset): Opt into bounded
            adaptive chart positions from exact timestamps through days. Omit for the legacy fixed
            daily grid.
        limit (int | Unset): Maximum target-agent rows to return. Defaults to 25. Default: 25.
        page_token (str | Unset): Opaque signed continuation bound to the organization, frozen
            watermark, range, evaluator, singular table target, and effective limit. Comparison
            agents, versions, and metric may change without resetting the table page. Expires after
            one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse]
     """


    kwargs = _get_kwargs(
        range_=range_,
evaluator_agent_version_id=evaluator_agent_version_id,
target_agent_id=target_agent_id,
series_target_agent_id=series_target_agent_id,
series_previous_target_agent_version_id=series_previous_target_agent_version_id,
series_metric=series_metric,
series_criterion_key=series_criterion_key,
series_resolution=series_resolution,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    range_: GetEvaluationOverviewRange | Unset = GetEvaluationOverviewRange.VALUE_1,
    evaluator_agent_version_id: UUID,
    target_agent_id: UUID | Unset = UNSET,
    series_target_agent_id: list[UUID] | Unset = UNSET,
    series_previous_target_agent_version_id: list[UUID] | Unset = UNSET,
    series_metric: GetEvaluationOverviewSeriesMetric | Unset = GetEvaluationOverviewSeriesMetric.OVERALL,
    series_criterion_key: str | Unset = UNSET,
    series_resolution: GetEvaluationOverviewSeriesResolution | Unset = UNSET,
    limit: int | Unset = 25,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse | None:
    """ Get evaluation overview

     Returns one server-composed evaluation dashboard page from a fixed batch of strong-snapshot reads at
    the durable analytics watermark. Current and prior windows are adjacent and equal; cohort history
    gaps produce explicit null coverage fields rather than misleading zeroes.

    Args:
        range_ (GetEvaluationOverviewRange | Unset): Length of the current window. The prior
            window is the adjacent interval of equal length. Default:
            GetEvaluationOverviewRange.VALUE_1.
        evaluator_agent_version_id (UUID): Immutable evaluation-agent version whose rubric and
            verdicts define this overview.
        target_agent_id (UUID | Unset): Optionally narrow page-level metrics, table rows, and
            retained history to one target agent.
        series_target_agent_id (list[UUID] | Unset): Repeat to explicitly compare up to five
            target agents; absent values select the page target or the first five whole-filter agents.
        series_previous_target_agent_version_id (list[UUID] | Unset): Repeat to add scoped
            previous target-agent versions; automatic latest versions plus these values may total at
            most twelve traces.
        series_metric (GetEvaluationOverviewSeriesMetric | Unset): Verdict population plotted for
            each selected target-agent version. Default: GetEvaluationOverviewSeriesMetric.OVERALL.
        series_criterion_key (str | Unset): Rubric key plotted when series_metric is criterion;
            required exactly for that metric.
        series_resolution (GetEvaluationOverviewSeriesResolution | Unset): Opt into bounded
            adaptive chart positions from exact timestamps through days. Omit for the legacy fixed
            daily grid.
        limit (int | Unset): Maximum target-agent rows to return. Defaults to 25. Default: 25.
        page_token (str | Unset): Opaque signed continuation bound to the organization, frozen
            watermark, range, evaluator, singular table target, and effective limit. Comparison
            agents, versions, and metric may change without resetting the table page. Expires after
            one hour.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsEvaluationOverviewResponse
     """


    return (await asyncio_detailed(
        client=client,
range_=range_,
evaluator_agent_version_id=evaluator_agent_version_id,
target_agent_id=target_agent_id,
series_target_agent_id=series_target_agent_id,
series_previous_target_agent_version_id=series_previous_target_agent_version_id,
series_metric=series_metric,
series_criterion_key=series_criterion_key,
series_resolution=series_resolution,
limit=limit,
page_token=page_token,

    )).parsed
