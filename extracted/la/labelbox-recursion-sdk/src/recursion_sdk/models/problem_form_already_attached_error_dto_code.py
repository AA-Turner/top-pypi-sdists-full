from enum import StrEnum

class ProblemFormAlreadyAttachedErrorDtoCode(StrEnum):
    PROBLEM_FORM_ALREADY_ATTACHED = "problem_form_already_attached"

    def __str__(self) -> str:
        return str(self.value)
