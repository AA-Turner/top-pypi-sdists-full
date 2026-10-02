from enum import StrEnum

class ManagedAgentsEvaluationTargetSkippedReasonCode(StrEnum):
    CHILD_CREATE_FAILED = "child_create_failed"
    CHILD_RUN_FAILED = "child_run_failed"
    CLEANUP_OR_ACCOUNTING_FAILED = "cleanup_or_accounting_failed"
    VERDICT_INVALID = "verdict_invalid"

    def __str__(self) -> str:
        return str(self.value)
