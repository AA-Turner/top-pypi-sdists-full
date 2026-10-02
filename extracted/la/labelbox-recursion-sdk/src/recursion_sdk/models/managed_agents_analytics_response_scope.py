from enum import StrEnum

class ManagedAgentsAnalyticsResponseScope(StrEnum):
    GLOBAL = "global"
    TENANT = "tenant"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
