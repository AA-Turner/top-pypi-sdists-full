"""Typed failure preserving admission diagnostics or an unsuccessful captured execution cycle."""

from labqoat._generated.recovery_operation import RecoveryOperation
from labqoat.errors.api_error import ApiError


class RecoveryFailedError(ApiError):
    """Retain operation identity when recovery fails before or after allocating an attempt."""

    def __init__(self, operation: RecoveryOperation) -> None:
        """Report admission and execution independently without reading a newer Run projection."""
        super().__init__(
            f"Recovery {operation.id}: admission {operation.phase}, execution {operation.execution_outcome or 'not completed'}."
        )
        self.operation = operation
