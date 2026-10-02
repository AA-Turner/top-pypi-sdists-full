from enum import StrEnum

class ManagedAgentsApiErrorManagedAgentsUnavailableCode(StrEnum):
    MANAGED_AGENTS_UNAVAILABLE = "managed_agents_unavailable"

    def __str__(self) -> str:
        return str(self.value)
