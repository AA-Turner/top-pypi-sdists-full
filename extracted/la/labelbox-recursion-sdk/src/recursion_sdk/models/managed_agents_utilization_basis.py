from enum import StrEnum

class ManagedAgentsUtilizationBasis(StrEnum):
    AGENT_HISTORY = "agent_history"
    WORKLOAD_PRIOR = "workload_prior"

    def __str__(self) -> str:
        return str(self.value)
