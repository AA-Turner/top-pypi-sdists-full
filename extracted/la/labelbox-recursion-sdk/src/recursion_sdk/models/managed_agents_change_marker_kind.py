from enum import StrEnum

class ManagedAgentsChangeMarkerKind(StrEnum):
    AGENT_VERSION = "agent_version"
    MODEL_CHANGE = "model_change"

    def __str__(self) -> str:
        return str(self.value)
