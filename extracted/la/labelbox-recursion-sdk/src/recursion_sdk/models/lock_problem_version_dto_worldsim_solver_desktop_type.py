from enum import StrEnum

class LockProblemVersionDtoWorldsimSolverDesktopType(StrEnum):
    CHROME = "chrome"
    FULL_DESKTOP = "full_desktop"

    def __str__(self) -> str:
        return str(self.value)
