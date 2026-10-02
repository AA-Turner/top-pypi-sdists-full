from enum import StrEnum

class ManagedAgentsApiErrorSetupRunsUnavailableCode(StrEnum):
    SETUP_RUNS_UNAVAILABLE = "setup_runs_unavailable"

    def __str__(self) -> str:
        return str(self.value)
