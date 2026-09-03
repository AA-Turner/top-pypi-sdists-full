"""Public re-export shim for idempotency primitives.

Provides the path named in issue #1883 deliverables while keeping
canonical implementations in their existing modules.
"""

import json

from agentic_devtools.orchestration.execution.idempotency import (
    IdempotencyRegistry,
)
from agentic_devtools.orchestration.safety.operation_id import (
    compute_operation_id,
)
from agentic_devtools.orchestration.safety.operation_log import (
    OperationLog,
    OperationLogRecord,
)

__all__ = [
    "IdempotencyRegistry",
    "OperationLog",
    "OperationLogRecord",
    "compute_operation_id",
    "is_reconciliation_run_duplicate",
]


class IdempotencyStateUnknownError(RuntimeError):
    """Raised when the completion log cannot be read or decoded safely."""


_TERMINAL_STATUSES = frozenset(("success", "completed"))
_PENDING_STATUSES = frozenset(("pending",))


def is_reconciliation_run_duplicate(
    operation_log: OperationLog,
    run_id: str,
    operation_id: str,
) -> bool:
    """Return True if a reconciliation action is already recorded as complete."""
    record: OperationLogRecord | None = operation_log.lookup(operation_id)
    if record is not None and record.run_id == run_id:
        if record.status in _TERMINAL_STATUSES:
            return True
        if record.status in _PENDING_STATUSES:
            raise IdempotencyStateUnknownError(
                f"Operation {operation_id!r} is already pending in run {run_id!r}; outcome is unknown"
            )
    if not operation_log.log_path.exists():
        raise IdempotencyStateUnknownError(f"Idempotency log is unavailable: {operation_log.log_path}")
    try:
        content = operation_log.log_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise IdempotencyStateUnknownError(f"Idempotency log could not be read: {operation_log.log_path}") from None
    for line in reversed(content.splitlines()):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise IdempotencyStateUnknownError("Idempotency log contains malformed JSON") from exc
        if not isinstance(parsed, dict):
            raise IdempotencyStateUnknownError("Idempotency log contains non-object JSON entries")
        if parsed.get("operation_id") != operation_id:
            continue
        try:
            prior = OperationLogRecord.from_dict(parsed)
        except (TypeError, KeyError, ValueError) as exc:
            raise IdempotencyStateUnknownError("Idempotency log contains malformed operation records") from exc
        if prior.status in _TERMINAL_STATUSES:
            return True
        if prior.status in _PENDING_STATUSES:
            raise IdempotencyStateUnknownError(
                f"Operation {operation_id!r} has a pending record in the idempotency log; outcome is unknown"
            )
        if prior.status not in {"failed", "skipped"}:
            raise IdempotencyStateUnknownError(
                f"Operation {operation_id!r} has unrecognized status {prior.status!r}; outcome is unknown"
            )
    return False
