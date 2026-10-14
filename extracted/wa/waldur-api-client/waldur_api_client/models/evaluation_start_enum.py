from enum import Enum


class EvaluationStartEnum(str, Enum):
    AT_CUTOFF = "at_cutoff"
    ON_SUBMISSION = "on_submission"

    def __str__(self) -> str:
        return str(self.value)
