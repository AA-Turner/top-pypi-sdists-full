# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for ``geneva.jobs.types`` — :class:`Job` and the
:class:`JobResult` hierarchy. Covers payload normalization,
job_id correlation, and per-result-class kwarg filtering."""

from __future__ import annotations

from typing import Any

from geneva.jobs.types import (
    DONE,
    BackfillJobResult,
    Job,
    JobResult,
    RefreshJobResult,
    UdfResult,
)
from geneva.table import JobFuture


class _StubFuture(JobFuture):
    """Minimal JobFuture that yields a pre-baked payload."""

    def __init__(self, job_id: str, payload: Any) -> None:
        self.job_id = job_id
        self._payload = payload

    def done(self, timeout: float | None = None) -> bool:
        return True

    def result(self, timeout: float | None = None) -> Any:
        return self._payload

    def status(self, timeout: float | None = None) -> None:
        return None


class TestJobBuildResult:
    def test_backfill_payload_promotes_to_columns_dict(self) -> None:
        """Wire-format payload (flat ``column_name`` + ``udf_name`` +
        counters) is folded into ``columns: dict[str, UdfResult]``.
        Refresh-only keys are filtered out."""
        payload = {
            "job_id": "j1",
            "table_name": "t",
            "column_name": "c",
            "input_columns": ["MetaData.UserId"],
            "udf_name": "embed",
            "udf_version": "v1",
            "rows_processed": 10,
            "rows_skipped": 0,
            "rows_refreshed": 99,
            "new_source_fragments": 3,
        }
        future = _StubFuture("j1", payload)
        job = Job(
            future, table_name="t", column_names=["c"], result_cls=BackfillJobResult
        )
        result = job.result()
        assert isinstance(result, BackfillJobResult)
        assert set(result.columns) == {"c"}
        udf = result.columns["c"]
        assert udf.udf_name == "embed"
        assert udf.udf_version == "v1"
        assert udf.input_columns == ["MetaData.UserId"]
        assert udf.rows_processed == 10
        assert udf.rows_skipped == 0

    def test_backfill_payload_uses_output_columns_when_job_has_no_column_names(
        self,
    ) -> None:
        payload = {
            "job_id": "j1",
            "table_name": "t",
            "input_columns": ["MetaData.UserId"],
            "output_columns": ["user_id"],
            "udf_name": "embed",
            "udf_version": "v1",
            "rows_processed": 10,
            "rows_skipped": 2,
        }
        future = _StubFuture("j1", payload)
        job = Job(future, table_name="t", result_cls=BackfillJobResult)
        result = job.result()

        assert isinstance(result, BackfillJobResult)
        assert set(result.columns) == {"user_id"}
        udf = result.columns["user_id"]
        assert udf.input_columns == ["MetaData.UserId"]
        assert udf.rows_processed == 10
        assert udf.rows_skipped == 2

    def test_refresh_payload_filters_backfill_only_keys(self) -> None:
        payload = {
            "job_id": "j2",
            "table_name": "t",
            "rows_refreshed": 50,
            "new_source_fragments": 4,
            "rows_processed": 10,
            "rows_skipped": 1,
            "column_name": "c",
            "udf_name": "embed",
        }
        future = _StubFuture("j2", payload)
        job = Job(future, table_name="t", result_cls=RefreshJobResult)
        result = job.result()
        assert isinstance(result, RefreshJobResult)
        assert result.rows_refreshed == 50
        assert result.new_source_fragments == 4

    def test_typed_payload_job_id_overridden_to_match_job(self) -> None:
        """Inner future returning a typed JobResult with its own uuid
        gets the outer Job's job_id stamped on it."""
        inner = RefreshJobResult(
            job_id="inner-uuid",
            status=DONE,
            table_name="t",
            rows_refreshed=7,
        )
        future = _StubFuture("outer-uuid", inner)
        job = Job(future, table_name="t", result_cls=RefreshJobResult)
        result = job.result()
        assert result.job_id == "outer-uuid"
        assert result.rows_refreshed == 7

    def test_typed_payload_with_matching_job_id_passed_through(self) -> None:
        inner = BackfillJobResult(
            job_id="same-uuid",
            status=DONE,
            table_name="t",
            columns={"c": UdfResult(rows_processed=5)},
        )
        future = _StubFuture("same-uuid", inner)
        job = Job(
            future, table_name="t", column_names=["c"], result_cls=BackfillJobResult
        )
        result = job.result()
        assert result is inner


class TestBackfillJobResultColumnsAccess:
    def test_single_column(self) -> None:
        result = BackfillJobResult(
            job_id="j",
            status=DONE,
            table_name="t",
            columns={"c": UdfResult(udf_name="embed", rows_processed=42)},
        )
        assert set(result.columns) == {"c"}
        assert result.columns["c"].udf_name == "embed"
        assert result.columns["c"].rows_processed == 42

    def test_multi_column(self) -> None:
        result = BackfillJobResult(
            job_id="j",
            status=DONE,
            table_name="t",
            columns={
                "a": UdfResult(udf_name="ua", rows_processed=10),
                "b": UdfResult(udf_name="ub", rows_processed=20),
            },
        )
        assert set(result.columns) == {"a", "b"}
        assert result.columns["a"].rows_processed == 10
        assert result.columns["b"].rows_processed == 20

    def test_zero_columns(self) -> None:
        result = BackfillJobResult(job_id="j", status=DONE, table_name="t")
        assert result.columns == {}


def test_udf_result_positional_args_remain_backward_compatible() -> None:
    result = UdfResult("embed", "v1", 10, 2)

    assert result.udf_name == "embed"
    assert result.udf_version == "v1"
    assert result.rows_processed == 10
    assert result.rows_skipped == 2
    assert result.input_columns is None


def test_job_class_module_export() -> None:
    """Sanity: Job and the result types are importable from the
    canonical public path."""
    import geneva

    assert geneva.Job is Job
    assert geneva.JobResult is JobResult
    assert geneva.BackfillJobResult is BackfillJobResult
    assert geneva.RefreshJobResult is RefreshJobResult
