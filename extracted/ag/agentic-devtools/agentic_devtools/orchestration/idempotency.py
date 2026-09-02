"""Public re-export shim for idempotency primitives.

Provides the path named in issue #1883 deliverables while keeping
canonical implementations in their existing modules.
"""

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
]
