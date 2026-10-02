from enum import StrEnum

class FormProblemVersionLockedErrorDtoCode(StrEnum):
    FORM_PROBLEM_VERSION_LOCKED = "form_problem_version_locked"

    def __str__(self) -> str:
        return str(self.value)
