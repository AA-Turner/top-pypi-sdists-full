from enum import StrEnum

class RunConfigReadinessDtoSolverMenuIssueType0(StrEnum):
    MISSING = "missing"
    STALE = "stale"

    def __str__(self) -> str:
        return str(self.value)
