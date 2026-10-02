from enum import StrEnum

class ProblemRunExecutionEvidenceDtoHandoffCloneFromRunIdStatus(StrEnum):
    MISSING = "missing"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
