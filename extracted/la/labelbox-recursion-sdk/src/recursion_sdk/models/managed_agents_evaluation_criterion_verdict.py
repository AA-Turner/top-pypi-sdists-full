from enum import StrEnum

class ManagedAgentsEvaluationCriterionVerdict(StrEnum):
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    PASS = "pass"

    def __str__(self) -> str:
        return str(self.value)
