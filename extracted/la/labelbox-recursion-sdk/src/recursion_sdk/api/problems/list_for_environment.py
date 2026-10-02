from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_for_environment_avg_score_metric import ListForEnvironmentAvgScoreMetric
from ...models.list_for_environment_sort_by import ListForEnvironmentSortBy
from ...models.list_for_environment_sort_direction import ListForEnvironmentSortDirection
from ...models.problem_list_items_response_dto import ProblemListItemsResponseDto
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_direction: ListForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: ListForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,
    sort_by: ListForEnvironmentSortBy | Unset = UNSET,
    sort_by_enrichment: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort_direction: str | Unset = UNSET
    if not isinstance(sort_direction, Unset):
        json_sort_direction = sort_direction.value

    params["sortDirection"] = json_sort_direction

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

    json_sort_by: str | Unset = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    params["sortByEnrichment"] = sort_by_enrichment


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/environments/{environment_id}/problem-list-items".format(environment_id=quote(str(environment_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = ProblemListItemsResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_direction: ListForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: ListForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,
    sort_by: ListForEnvironmentSortBy | Unset = UNSET,
    sort_by_enrichment: str | Unset = UNSET,

) -> Response[ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List problems with per-row aggregates (table view)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_direction (ListForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (ListForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg, min, or
            max) the score bounds apply to. Defaults to the average.
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
        sort_by (ListForEnvironmentSortBy | Unset): Local sort column. Mutually exclusive with the
            enrichment sort axis.
        sort_by_enrichment (str | Unset): Enrichment-dimension key (e.g. workflow, priority) to
            sort by. Mutually exclusive with the local sort column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,
cursor=cursor,
sort_direction=sort_direction,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,
sort_by=sort_by,
sort_by_enrichment=sort_by_enrichment,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_direction: ListForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: ListForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,
    sort_by: ListForEnvironmentSortBy | Unset = UNSET,
    sort_by_enrichment: str | Unset = UNSET,

) -> ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List problems with per-row aggregates (table view)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_direction (ListForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (ListForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg, min, or
            max) the score bounds apply to. Defaults to the average.
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
        sort_by (ListForEnvironmentSortBy | Unset): Local sort column. Mutually exclusive with the
            enrichment sort axis.
        sort_by_enrichment (str | Unset): Enrichment-dimension key (e.g. workflow, priority) to
            sort by. Mutually exclusive with the local sort column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
limit=limit,
cursor=cursor,
sort_direction=sort_direction,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,
sort_by=sort_by,
sort_by_enrichment=sort_by_enrichment,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_direction: ListForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: ListForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,
    sort_by: ListForEnvironmentSortBy | Unset = UNSET,
    sort_by_enrichment: str | Unset = UNSET,

) -> Response[ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List problems with per-row aggregates (table view)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_direction (ListForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (ListForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg, min, or
            max) the score bounds apply to. Defaults to the average.
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
        sort_by (ListForEnvironmentSortBy | Unset): Local sort column. Mutually exclusive with the
            enrichment sort axis.
        sort_by_enrichment (str | Unset): Enrichment-dimension key (e.g. workflow, priority) to
            sort by. Mutually exclusive with the local sort column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,
cursor=cursor,
sort_direction=sort_direction,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,
sort_by=sort_by,
sort_by_enrichment=sort_by_enrichment,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_direction: ListForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    models: list[str] | Unset = UNSET,
    avg_score_metric: ListForEnvironmentAvgScoreMetric | Unset = UNSET,
    avg_score_min: float | Unset = UNSET,
    avg_score_max: float | Unset = UNSET,
    created_at_from: datetime.date | Unset = UNSET,
    created_at_to: datetime.date | Unset = UNSET,
    enrichment_filters: str | Unset = UNSET,
    sort_by: ListForEnvironmentSortBy | Unset = UNSET,
    sort_by_enrichment: str | Unset = UNSET,

) -> ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List problems with per-row aggregates (table view)

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_direction (ListForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text search filter applied across problem title and external
            id.
        models (list[str] | Unset): Comma-separated list of model identifiers; matches problems
            with at least one run on any listed model.
        avg_score_metric (ListForEnvironmentAvgScoreMetric | Unset): Which aggregate (avg, min, or
            max) the score bounds apply to. Defaults to the average.
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
        sort_by (ListForEnvironmentSortBy | Unset): Local sort column. Mutually exclusive with the
            enrichment sort axis.
        sort_by_enrichment (str | Unset): Enrichment-dimension key (e.g. workflow, priority) to
            sort by. Mutually exclusive with the local sort column.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProblemListItemsResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
limit=limit,
cursor=cursor,
sort_direction=sort_direction,
search=search,
models=models,
avg_score_metric=avg_score_metric,
avg_score_min=avg_score_min,
avg_score_max=avg_score_max,
created_at_from=created_at_from,
created_at_to=created_at_to,
enrichment_filters=enrichment_filters,
sort_by=sort_by,
sort_by_enrichment=sort_by_enrichment,

    )).parsed
