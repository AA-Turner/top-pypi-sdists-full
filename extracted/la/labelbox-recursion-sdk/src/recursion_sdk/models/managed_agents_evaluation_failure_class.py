from enum import StrEnum

class ManagedAgentsEvaluationFailureClass(StrEnum):
    CRITERION_FAILURE = "criterion_failure"
    INCOMPLETE = "incomplete"
    MULTIPLE_CRITERIA = "multiple_criteria"
    NONE = "none"
    OUT_OF_SCOPE = "out_of_scope"
    TARGET_CANCELLED = "target_cancelled"
    TARGET_FAILED = "target_failed"
    TERMINATION = "termination"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    UNVERIFIED = "unverified"

    def __str__(self) -> str:
        return str(self.value)
