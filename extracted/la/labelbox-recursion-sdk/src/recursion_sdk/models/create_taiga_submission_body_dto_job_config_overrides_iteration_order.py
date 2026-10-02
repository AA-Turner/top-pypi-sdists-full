from enum import StrEnum

class CreateTaigaSubmissionBodyDtoJobConfigOverridesIterationOrder(StrEnum):
    ATTEMPTS_FIRST = "attempts_first"
    PROBLEMS_FIRST = "problems_first"

    def __str__(self) -> str:
        return str(self.value)
