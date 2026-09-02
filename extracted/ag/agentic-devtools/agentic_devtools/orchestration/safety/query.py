"""Query surface for operation log and audit entries (FR-010).

Provides read-only query APIs for programmatic inspection of the
operation log and audit entries. These never participate in
control-flow decisions.
"""

from __future__ import annotations

import logging
from typing import Any

from .operation_log import OperationLog, OperationLogRecord

logger = logging.getLogger(__name__)


def query_operation_log(
    operation_log: OperationLog,
    *,
    tool_name: str | None = None,
    status: str | None = None,
    run_id: str | None = None,
    limit: int | None = None,
) -> list[OperationLogRecord]:
    """Query the operation log with optional filters.

    Filters are applied conjunctively (AND semantics).
    Results are returned in index order (last-wins for same operation_id).

    Args:
        operation_log: The OperationLog instance to query.
        tool_name: Filter by tool name (exact match).
        status: Filter by status (exact match).
        run_id: Filter by run_id. Must match the current run_id held by the
            OperationLog instance. Mismatches raise ValueError because
            OperationLog is already scoped to a single run_id.
        limit: Maximum number of results to return.

    Returns:
        List of matching OperationLogRecord entries.
    """
    records = operation_log.all_records()

    if tool_name is not None:
        records = [r for r in records if r.tool_name == tool_name]
    if status is not None:
        records = [r for r in records if r.status == status]
    if run_id is not None and run_id != operation_log.run_id:
        raise ValueError(
            f"run_id '{run_id}' does not match OperationLog run_id '{operation_log.run_id}'",
        )
    if limit is not None:
        records = records[:limit]

    return records


def read_audit_entries(
    *,
    logger_name: str = "agentic_devtools.orchestration.tools.audit",
    limit: int | None = None,
) -> dict[str, Any]:
    """Read captured audit entries from the audit logger.

    Since audit entries are emitted via Python logging (not persisted to
    a dedicated file), this function returns availability information
    and any entries that can be read from a configured handler.

    Returns:
        A dict with:
        - "available": bool indicating if entries can be read
        - "entries": list of parsed audit entry dicts (empty if unavailable)
        - "message": explanation when unavailable
    """
    audit_logger = logging.getLogger(logger_name)

    # Check if any handler has captured entries (e.g., a MemoryHandler for testing)
    for handler in audit_logger.handlers:
        if hasattr(handler, "buffer"):
            # MemoryHandler or similar with a buffer
            import json

            entries = []
            for record in handler.buffer:
                try:
                    entry = json.loads(record.getMessage())
                    entries.append(entry)
                except (json.JSONDecodeError, AttributeError):
                    continue
            if limit is not None:
                entries = entries[:limit]
            return {"available": True, "entries": entries, "message": ""}

    return {
        "available": False,
        "entries": [],
        "message": (
            "Audit entries are emitted via Python logging. Configure a handler on the audit logger to capture them."
        ),
    }
