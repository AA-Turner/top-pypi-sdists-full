# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for reattaching to a running remote job by ID.

Exercises ``RemoteJob.from_job`` (rebuild a handle from the durable
``_geneva_jobs`` record so polling can resume after the original client exits)
and ``result()``'s logging: the job id on start, and resume instructions only
when polling stops for a client-side reason (not a server-side job failure).
Connections are mocked, so no phalanx/cluster is needed.
"""

import logging
from unittest.mock import MagicMock

import pytest

from geneva.jobs.jobs import JobRecord, JobStatus
from geneva.jobs.remote import RemoteJob

_RESUME_HINT = 'RemoteJob.from_job(conn, "job-xyz").result()'


def _record(
    job_id: str,
    *,
    status: JobStatus = JobStatus.RUNNING,
    table_name: str = "tbl",
    column_name: str | None = "col",
    job_type: str = "backfill",
    events: list[str] | None = None,
) -> JobRecord:
    return JobRecord(
        table_name=table_name,
        column_name=column_name,
        job_id=job_id,
        job_type=job_type,
        status=status,
        events=events or [],
    )


def test_from_job_rebuilds_handle_from_record() -> None:
    """The rehydrated handle carries the record's identity + a bound conn."""
    record = _record(
        "jid", table_name="my_table", column_name="emb", job_type="refresh"
    )
    conn = MagicMock()
    conn.get_job.return_value = record

    job = RemoteJob.from_job(conn, "jid")

    conn.get_job.assert_called_once_with("jid")
    assert job.job_id == "jid"
    assert job.table_name == "my_table"
    assert job.column_name == "emb"
    assert job.job_type == "refresh"
    assert job._conn is conn


def test_from_job_unknown_id_propagates_value_error() -> None:
    conn = MagicMock()
    conn.get_job.side_effect = ValueError("Job nope not found")
    with pytest.raises(ValueError, match="not found"):
        RemoteJob.from_job(conn, "nope")


def _run_result(conn: MagicMock, caplog) -> tuple[object, str]:
    """Drive result() with mocked bars (no real tqdm) and capture the logs."""
    job = RemoteJob(job_id="job-xyz", table_name="tbl", conn=conn)
    with caplog.at_level(logging.INFO, logger="geneva.jobs.remote"):
        exc: BaseException | None = None
        result = None
        try:
            result = job.result(bars=MagicMock())
        except BaseException as e:  # noqa: BLE001 - re-inspected by each test
            exc = e
    messages = "\n".join(rec.getMessage() for rec in caplog.records)
    return exc if exc is not None else result, messages


def test_result_logs_job_id_on_start_no_hint_on_success(caplog) -> None:
    """A job that completes logs its id on start and never the resume hint."""
    conn = MagicMock()
    conn.get_job.return_value = _record("job-xyz", status=JobStatus.DONE)

    result, messages = _run_result(conn, caplog)

    assert getattr(result, "job_id", None) == "job-xyz"
    assert "Polling remote job: job-xyz" in messages
    assert _RESUME_HINT not in messages


def test_result_logs_resume_hint_on_client_error(caplog) -> None:
    """A client-side polling failure (e.g. lost connection) surfaces how to
    reattach, since the server job may still be running."""
    conn = MagicMock()
    conn.get_job.side_effect = ConnectionError("transport down")

    result, messages = _run_result(conn, caplog)

    assert isinstance(result, ConnectionError)  # original error propagated
    assert _RESUME_HINT in messages


def test_result_no_resume_hint_on_server_failure(caplog) -> None:
    """A server-side job failure raises but does NOT print resume instructions
    -- there is nothing left to resume."""
    conn = MagicMock()
    conn.get_job.return_value = _record(
        "job-xyz", status=JobStatus.FAILED, events=["worker OOM"]
    )

    result, messages = _run_result(conn, caplog)

    assert isinstance(result, RuntimeError)
    assert "failed" in str(result)
    assert "Polling remote job: job-xyz" in messages  # start line still logged
    assert _RESUME_HINT not in messages


def test_dispatch_logs_job_id_on_start(caplog) -> None:
    """A freshly dispatched remote job logs its id at construction, so the sync
    backfill/load-columns drivers -- which only call result() after the job is
    already terminal -- still surface the id at job start (PR #1079 review)."""
    from geneva.remote_v2 import RemoteJobFuture

    job = RemoteJob(job_id="job-xyz", table_name="tbl", conn=MagicMock())
    with caplog.at_level(logging.INFO, logger="geneva.remote_v2"):
        RemoteJobFuture(job)

    messages = "\n".join(rec.getMessage() for rec in caplog.records)
    assert "Started remote job job-xyz" in messages
