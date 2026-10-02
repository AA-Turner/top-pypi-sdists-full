from enum import StrEnum

class ListSessionsEvaluationResult(StrEnum):
    EVALUATED = "evaluated"
    FAIL = "fail"
    NONE = "none"
    NOT_APPLICABLE = "not_applicable"
    PASS = "pass"

    def __str__(self) -> str:
        return str(self.value)
