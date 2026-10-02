from enum import StrEnum

class ManagedAgentsApiErrorIntegrationsUnconfiguredCode(StrEnum):
    INTEGRATIONS_UNCONFIGURED = "integrations_unconfigured"

    def __str__(self) -> str:
        return str(self.value)
