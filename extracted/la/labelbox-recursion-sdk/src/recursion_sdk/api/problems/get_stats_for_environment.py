from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_stats_for_environment_avg_score_metric import GetStatsForEnvironmentAvgScoreMetric
from ...models.problem_list_stats_dto import ProblemListStatsDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    environment_id: UUID,
    *,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: GetStatsForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["search"] = search

    json_models: list[str] | Unset = UNSET
    if not isinstance(models, Unset):
        json_models = models


    params["models"] = json_models

    json_avg_score_metric: str | Unset = UNSET
    if not isinstance(avg_score_metric, Unset):
        json_avg_score_metric = avg_score_metric.value

    params["avgScoreMetric"] = json_avg_score_metric

    params["avgScoreMin"] = avg_score_min

    params["avgScoreMax"] = avg_score_max

    json_created_at_from: str | Unset = UNSET
    if not isinstance(created_at_from, Unset):
        json_created_at_from = created_at_from.isoformat()
    params["createdAtFrom"] = json_created_at_from

    json_created_at_to: str | Unset = UNSET
    if not isinstance(created_at_to, Unset):
        json_created_at_to = created_at_to.isoformat()
    params["createdAtTo"] = json_created_at_to

    params["enrichmentFilters"] = enrichment_filters


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/environments/{environment_id}/problem-list-stats".format(environment_id=quote(str(environment_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = ProblemListStatsDto.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = TargetApiErrorRateLimitExceeded.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> TargetApiErrorInternalError | TargetApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = TargetApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = TargetApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: GetStatsForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,

) -> Response[ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Aggregate stats over filtered problems (env-overview KPIs)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (GetStatsForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg,
            min, or max) the score bounds apply to. Defaults to the average.
        avg_score_min (float | Unset): Inclusive lower bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 25.
        avg_score_max (float | Unset): Inclusive upper bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 75.
        created_at_from (datetime.date | Unset): Inclusive lower bound on problem creation date,
            in YYYY-MM-DD form (UTC calendar day).
        created_at_to (datetime.date | Unset): Inclusive upper bound on problem creation date, in
            YYYY-MM-DD form (UTC calendar day).
        enrichment_filters (str | Unset): JSON-encoded enrichment-dimension filters. Send one
            query-string value containing a JSON object that maps dimension names to allowed string
            values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: GetStatsForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,

) -> ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Aggregate stats over filtered problems (env-overview KPIs)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (GetStatsForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg,
            min, or max) the score bounds apply to. Defaults to the average.
        avg_score_min (float | Unset): Inclusive lower bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 25.
        avg_score_max (float | Unset): Inclusive upper bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 75.
        created_at_from (datetime.date | Unset): Inclusive lower bound on problem creation date,
            in YYYY-MM-DD form (UTC calendar day).
        created_at_to (datetime.date | Unset): Inclusive upper bound on problem creation date, in
            YYYY-MM-DD form (UTC calendar day).
        enrichment_filters (str | Unset): JSON-encoded enrichment-dimension filters. Send one
            query-string value containing a JSON object that maps dimension names to allowed string
            values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: GetStatsForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,

) -> Response[ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Aggregate stats over filtered problems (env-overview KPIs)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (GetStatsForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg,
            min, or max) the score bounds apply to. Defaults to the average.
        avg_score_min (float | Unset): Inclusive lower bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 25.
        avg_score_max (float | Unset): Inclusive upper bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 75.
        created_at_from (datetime.date | Unset): Inclusive lower bound on problem creation date,
            in YYYY-MM-DD form (UTC calendar day).
        created_at_to (datetime.date | Unset): Inclusive upper bound on problem creation date, in
            YYYY-MM-DD form (UTC calendar day).
        enrichment_filters (str | Unset): JSON-encoded enrichment-dimension filters. Send one
            query-string value containing a JSON object that maps dimension names to allowed string
            values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: GetStatsForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,

) -> ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Aggregate stats over filtered problems (env-overview KPIs)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (GetStatsForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg,
            min, or max) the score bounds apply to. Defaults to the average.
        avg_score_min (float | Unset): Inclusive lower bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 25.
        avg_score_max (float | Unset): Inclusive upper bound on the selected score metric,
            expressed as a 0–100 percentage. Example: 75.
        created_at_from (datetime.date | Unset): Inclusive lower bound on problem creation date,
            in YYYY-MM-DD form (UTC calendar day).
        created_at_to (datetime.date | Unset): Inclusive upper bound on problem creation date, in
            YYYY-MM-DD form (UTC calendar day).
        enrichment_filters (str | Unset): JSON-encoded enrichment-dimension filters. Send one
            query-string value containing a JSON object that maps dimension names to allowed string
            values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemListStatsDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,

    )).parsed
