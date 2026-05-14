"""Derive dataframe run status from raw shard/attempt data.

Mirror of go-api-server/dataframe/derive.go and
frontend/components/dataframe-runs/deriveDataFrameRunStatus.ts. Keep all
three implementations in sync — the rules are documented in the proto
file's comments on DataFrameRun and DataFrameRunAttempt.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRun, DataFrameRunAttempt, DataFrameRunShard


def derive_dataframe_run_status(run: "DataFrameRun"):
    """Compute the user-visible status of a run from its shards and attempts.

    A failed attempt with attempts.length < max_attempts is treated as QUEUED
    (the queue will retry). Precedence across shards:
    FAILED > CANCELED > WORKING > STARTING > QUEUED, with COMPLETED only when
    every shard is COMPLETED.
    """
    from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRunStatus

    if not run.shards:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED

    has_failed = has_canceled = has_working = has_starting = False
    all_completed = True
    for shard in run.shards:
        s = _derive_shard_status(shard)
        if s == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED:
            has_failed = True
            all_completed = False
        elif s == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED:
            has_canceled = True
            all_completed = False
        elif s == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING:
            has_working = True
            all_completed = False
        elif s == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_STARTING:
            has_starting = True
            all_completed = False
        elif s != DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED:
            all_completed = False

    if has_failed:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED
    if has_canceled:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED
    if has_working:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING
    if has_starting:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_STARTING
    if all_completed:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED
    return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED


def _derive_shard_status(shard: "DataFrameRunShard"):
    from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRunStatus, JobAttemptState

    terminal = (
        DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED,
        DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED,
        DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED,
    )
    if shard.status in terminal:
        return shard.status
    if not shard.attempts:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED
    latest = shard.attempts[-1]
    if latest.state == JobAttemptState.JOB_ATTEMPT_STATE_COMPLETED:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED
    if latest.state == JobAttemptState.JOB_ATTEMPT_STATE_CANCELED:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED
    if latest.state == JobAttemptState.JOB_ATTEMPT_STATE_FAILED:
        if len(shard.attempts) >= shard.max_attempts:
            return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED
    if latest.state == JobAttemptState.JOB_ATTEMPT_STATE_RUNNING:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING
    if latest.state == JobAttemptState.JOB_ATTEMPT_STATE_QUEUED:
        return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_STARTING
    return DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED


def latest_attempt(run: "DataFrameRun") -> Optional["DataFrameRunAttempt"]:
    """Highest-attempt_idx attempt across all shards, or None if none exist."""
    latest: Optional["DataFrameRunAttempt"] = None
    for shard in run.shards:
        for a in shard.attempts:
            if latest is None or a.attempt_idx > latest.attempt_idx:
                latest = a
    return latest
