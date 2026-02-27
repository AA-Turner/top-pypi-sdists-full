#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Dry run report collector for workload compatibility validation.

Collects information during dry run mode about:
- Successfully translated operations
- Unsupported operations / functions
- Generated Snowflake SQL and EXPLAIN validation results
- Schema information
"""

import json
import threading
from dataclasses import dataclass
from enum import Enum


class DryRunStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


@dataclass
class DryRunEntry:
    """A single entry in the dry run report."""

    operation: str
    status: DryRunStatus
    detail: str = ""
    generated_sql: str | None = None
    schema_info: str | None = None


class DryRunReport:
    """
    Thread-local report that accumulates dry run results across multiple
    ExecutePlan calls within a session.
    """

    def __init__(self) -> None:
        self._entries: list[DryRunEntry] = []
        self._lock = threading.RLock()

    def record_success(
        self,
        operation: str,
        detail: str = "",
        generated_sql: str | None = None,
        schema_info: str | None = None,
    ) -> None:
        with self._lock:
            self._entries.append(
                DryRunEntry(
                    operation=operation,
                    status=DryRunStatus.PASS,
                    detail=detail,
                    generated_sql=generated_sql,
                    schema_info=schema_info,
                )
            )

    def record_failure(
        self,
        operation: str,
        detail: str,
        generated_sql: str | None = None,
    ) -> None:
        with self._lock:
            self._entries.append(
                DryRunEntry(
                    operation=operation,
                    status=DryRunStatus.FAIL,
                    detail=detail,
                    generated_sql=generated_sql,
                )
            )

    def record_warning(
        self,
        operation: str,
        detail: str,
        generated_sql: str | None = None,
    ) -> None:
        with self._lock:
            self._entries.append(
                DryRunEntry(
                    operation=operation,
                    status=DryRunStatus.WARNING,
                    detail=detail,
                    generated_sql=generated_sql,
                )
            )

    @property
    def overall_status(self) -> DryRunStatus:
        with self._lock:
            if any(e.status == DryRunStatus.FAIL for e in self._entries):
                return DryRunStatus.FAIL
            if any(e.status == DryRunStatus.WARNING for e in self._entries):
                return DryRunStatus.WARNING
            return DryRunStatus.PASS

    @property
    def entries(self) -> list[DryRunEntry]:
        with self._lock:
            return list(self._entries)

    def to_json(self) -> str:
        with self._lock:
            return json.dumps(
                {
                    "overall_status": self.overall_status.value,
                    "total_operations": len(self._entries),
                    "passed": sum(
                        1 for e in self._entries if e.status == DryRunStatus.PASS
                    ),
                    "failed": sum(
                        1 for e in self._entries if e.status == DryRunStatus.FAIL
                    ),
                    "warnings": sum(
                        1
                        for e in self._entries
                        if e.status == DryRunStatus.WARNING
                    ),
                    "entries": [
                        {
                            "operation": e.operation,
                            "status": e.status.value,
                            "detail": e.detail,
                            "generated_sql": e.generated_sql,
                            "schema_info": e.schema_info,
                        }
                        for e in self._entries
                    ],
                },
                indent=2,
            )

    def to_summary_string(self) -> str:
        with self._lock:
            lines = []
            lines.append("=" * 60)
            lines.append(f"DRY RUN REPORT  [{self.overall_status.value}]")
            lines.append("=" * 60)

            passed = sum(
                1 for e in self._entries if e.status == DryRunStatus.PASS
            )
            failed = sum(
                1 for e in self._entries if e.status == DryRunStatus.FAIL
            )
            warned = sum(
                1 for e in self._entries if e.status == DryRunStatus.WARNING
            )
            lines.append(
                f"Operations: {len(self._entries)} total, "
                f"{passed} passed, {failed} failed, {warned} warnings"
            )
            lines.append("-" * 60)

            for i, entry in enumerate(self._entries, 1):
                marker = {
                    DryRunStatus.PASS: "OK ",
                    DryRunStatus.FAIL: "FAIL",
                    DryRunStatus.WARNING: "WARN",
                }[entry.status]
                lines.append(f"[{marker}] {i}. {entry.operation}")
                if entry.detail:
                    lines.append(f"       {entry.detail}")
                if entry.generated_sql:
                    sql_preview = entry.generated_sql[:120]
                    if len(entry.generated_sql) > 120:
                        sql_preview += "..."
                    lines.append(f"       SQL: {sql_preview}")
                if entry.schema_info:
                    lines.append(f"       Schema: {entry.schema_info}")

            lines.append("=" * 60)
            return "\n".join(lines)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


_session_reports: dict[str, DryRunReport] = {}
_reports_lock = threading.Lock()


def get_dryrun_report(session_id: str) -> DryRunReport:
    with _reports_lock:
        if session_id not in _session_reports:
            _session_reports[session_id] = DryRunReport()
        return _session_reports[session_id]


def clear_dryrun_report(session_id: str) -> None:
    with _reports_lock:
        if session_id in _session_reports:
            _session_reports[session_id].clear()
