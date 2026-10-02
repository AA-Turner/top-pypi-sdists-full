from enum import StrEnum

class EvaluationPageResponseDtoItemsItemKind(StrEnum):
    GRADE_ONLY = "grade_only"
    SOLVE_AND_GRADE = "solve_and_grade"

    def __str__(self) -> str:
        return str(self.value)
