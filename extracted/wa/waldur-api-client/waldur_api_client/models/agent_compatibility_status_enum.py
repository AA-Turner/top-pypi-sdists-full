from enum import Enum


class AgentCompatibilityStatusEnum(str, Enum):
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
