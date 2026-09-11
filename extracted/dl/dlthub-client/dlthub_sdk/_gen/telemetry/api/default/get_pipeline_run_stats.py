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
from ...models.pipeline_run_stats_response import PipelineRunStatsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    bucket: BucketSize | Unset = UNSET,
    pipeline_name: None | str | Unset = UNSET,
    dataset_name: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start = start.isoformat()
    params["start"] = json_start

    json_end = end.isoformat()
    params["end"] = json_end

    params["tz"] = tz

    json_bucket: str | Unset = UNSET
    if not isinstance(bucket, Unset):
        json_bucket = bucket.value

    params["bucket"] = json_bucket

    json_pipeline_name: None | str | Unset
    if isinstance(pipeline_name, Unset):
        json_pipeline_name = UNSET
    else:
        json_pipeline_name = pipeline_name
    params["pipeline_name"] = json_pipeline_name

    json_dataset_name: None | str | Unset
    if isinstance(dataset_name, Unset):
        json_dataset_name = UNSET
    else:
        json_dataset_name = dataset_name
    params["dataset_name"] = json_dataset_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/pipeline-runs/stats".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | PipelineRunStatsResponse | None:
    if response.status_code == 200:
        response_200 = PipelineRunStatsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | PipelineRunStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    bucket: BucketSize | Unset = UNSET,
    pipeline_name: None | str | Unset = UNSET,
    dataset_name: None | str | Unset = UNSET,
) -> Response[ErrorResponse400 | PipelineRunStatsResponse]:
    """GetPipelineRunStats

    Args:
        workspace_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        bucket (BucketSize | Unset): Bucket size for time series aggregation. 'all' returns a
            single entry covering the full period.
        pipeline_name (None | str | Unset):
        dataset_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | PipelineRunStatsResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        start=start,
        end=end,
        tz=tz,
        bucket=bucket,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    bucket: BucketSize | Unset = UNSET,
    pipeline_name: None | str | Unset = UNSET,
    dataset_name: None | str | Unset = UNSET,
) -> ErrorResponse400 | PipelineRunStatsResponse | None:
    """GetPipelineRunStats

    Args:
        workspace_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        bucket (BucketSize | Unset): Bucket size for time series aggregation. 'all' returns a
            single entry covering the full period.
        pipeline_name (None | str | Unset):
        dataset_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | PipelineRunStatsResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        start=start,
        end=end,
        tz=tz,
        bucket=bucket,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    bucket: BucketSize | Unset = UNSET,
    pipeline_name: None | str | Unset = UNSET,
    dataset_name: None | str | Unset = UNSET,
) -> Response[ErrorResponse400 | PipelineRunStatsResponse]:
    """GetPipelineRunStats

    Args:
        workspace_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        bucket (BucketSize | Unset): Bucket size for time series aggregation. 'all' returns a
            single entry covering the full period.
        pipeline_name (None | str | Unset):
        dataset_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | PipelineRunStatsResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        start=start,
        end=end,
        tz=tz,
        bucket=bucket,
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    bucket: BucketSize | Unset = UNSET,
    pipeline_name: None | str | Unset = UNSET,
    dataset_name: None | str | Unset = UNSET,
) -> ErrorResponse400 | PipelineRunStatsResponse | None:
    """GetPipelineRunStats

    Args:
        workspace_id (UUID):
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        bucket (BucketSize | Unset): Bucket size for time series aggregation. 'all' returns a
            single entry covering the full period.
        pipeline_name (None | str | Unset):
        dataset_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | PipelineRunStatsResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            start=start,
            end=end,
            tz=tz,
            bucket=bucket,
            pipeline_name=pipeline_name,
            dataset_name=dataset_name,
        )
    ).parsed
