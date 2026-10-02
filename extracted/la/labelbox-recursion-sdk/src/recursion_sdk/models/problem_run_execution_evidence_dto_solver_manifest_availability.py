from enum import StrEnum

class ProblemRunExecutionEvidenceDtoSolverManifestAvailability(StrEnum):
    AVAILABLE = "available"
    MISSING = "missing"
    UNAVAILABLE = "unavailable"
    UNREADABLE = "unreadable"

    def __str__(self) -> str:
        return str(self.value)
