from enum import StrEnum

class ProblemVersionFileListDtoItemType(StrEnum):
    GRADER_SUPPORT = "grader_support"
    PROBLEM = "problem"
    SUPPORTING = "supporting"

    def __str__(self) -> str:
        return str(self.value)
