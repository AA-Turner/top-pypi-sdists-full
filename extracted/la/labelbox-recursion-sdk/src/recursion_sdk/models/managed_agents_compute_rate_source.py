from enum import StrEnum

class ManagedAgentsComputeRateSource(StrEnum):
    AGENT_SERVICE_RATE_TABLE = "agent_service_rate_table"
    UNPRICED_ACCELERATOR = "unpriced_accelerator"

    def __str__(self) -> str:
        return str(self.value)
