from enum import StrEnum

class CreateTaigaSubmissionBodyDtoJobConfigOverridesPriority(StrEnum):
    HIGH = "high"
    LOW = "low"
    MAX = "max"

    def __str__(self) -> str:
        return str(self.value)
