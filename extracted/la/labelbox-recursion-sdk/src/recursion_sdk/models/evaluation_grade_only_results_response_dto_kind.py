from enum import StrEnum

class EvaluationGradeOnlyResultsResponseDtoKind(StrEnum):
    GRADE_ONLY = "grade_only"

    def __str__(self) -> str:
        return str(self.value)
