from enum import StrEnum

class CreateIssueBodyDtoEntityType(StrEnum):
    RUBRIC = "rubric"

    def __str__(self) -> str:
        return str(self.value)
