import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bucket_size import BucketSize
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.run_stats_response import RunStatsResponse
from ...types import UNSET, Response


def _get_kwargs(
    organization_id: UUID,
    *,
    start: datetime.datetime,
    end: datetime.datetime,
    bucket: BucketSize,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start = start.isoformat()
    params["start"] = json_start

    json_end = end.isoformat()
    params["end"] = json_end

    json_bucket = bucket.value
    params["bucket"] = json_bucket

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/organizations/{organization_id}/usage".format(
            organization_id=quote(str(organization_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
    | None
):
    if response.status_code == 200:
        response_200 = RunStatsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    bucket: BucketSize,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
]:
    """GetOrganizationUsage


    Get usage (run statistics) for an organization as time-bucketed breakdowns.

    Aggregates run metrics across all workspaces in the organization.
    Usage is always reckoned in UTC: `start`/`end` are naive datetimes interpreted as UTC, and
    bucket timestamps in the response are UTC.

    Requires MANAGE_ORG permission (owner role) on the organization.

    Args:
        organization_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        bucket (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry
            covering the full period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunStatsResponse]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        start=start,
        end=end,
        bucket=bucket,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    bucket: BucketSize,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
    | None
):
    """GetOrganizationUsage


    Get usage (run statistics) for an organization as time-bucketed breakdowns.

    Aggregates run metrics across all workspaces in the organization.
    Usage is always reckoned in UTC: `start`/`end` are naive datetimes interpreted as UTC, and
    bucket timestamps in the response are UTC.

    Requires MANAGE_ORG permission (owner role) on the organization.

    Args:
        organization_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        bucket (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry
            covering the full period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunStatsResponse
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        start=start,
        end=end,
        bucket=bucket,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    bucket: BucketSize,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
]:
    """GetOrganizationUsage


    Get usage (run statistics) for an organization as time-bucketed breakdowns.

    Aggregates run metrics across all workspaces in the organization.
    Usage is always reckoned in UTC: `start`/`end` are naive datetimes interpreted as UTC, and
    bucket timestamps in the response are UTC.

    Requires MANAGE_ORG permission (owner role) on the organization.

    Args:
        organization_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        bucket (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry
            covering the full period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunStatsResponse]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        start=start,
        end=end,
        bucket=bucket,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    bucket: BucketSize,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | RunStatsResponse
    | None
):
    """GetOrganizationUsage


    Get usage (run statistics) for an organization as time-bucketed breakdowns.

    Aggregates run metrics across all workspaces in the organization.
    Usage is always reckoned in UTC: `start`/`end` are naive datetimes interpreted as UTC, and
    bucket timestamps in the response are UTC.

    Requires MANAGE_ORG permission (owner role) on the organization.

    Args:
        organization_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        bucket (BucketSize): Bucket size for time series aggregation. 'all' returns a single entry
            covering the full period.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | RunStatsResponse
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            start=start,
            end=end,
            bucket=bucket,
        )
    ).parsed
