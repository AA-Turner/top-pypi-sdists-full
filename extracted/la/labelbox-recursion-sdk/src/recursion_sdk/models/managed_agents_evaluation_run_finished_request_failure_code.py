from enum import StrEnum

class ManagedAgentsEvaluationRunFinishedRequestFailureCode(StrEnum):
    ACCOUNTING_FAILED = "accounting_failed"
    AUDIT_FAILED = "audit_failed"
    CLEANUP_FAILED = "cleanup_failed"
    FINALIZATION_FAILED = "finalization_failed"
    PLAN_FAILED = "plan_failed"

    def __str__(self) -> str:
        return str(self.value)
