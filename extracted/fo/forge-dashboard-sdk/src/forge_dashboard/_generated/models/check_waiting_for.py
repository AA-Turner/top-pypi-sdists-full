from enum import StrEnum

class CheckWaitingFor(StrEnum):
    JOBS = "jobs"
    RUNNER = "runner"

    def __str__(self) -> str:
        return str(self.value)
