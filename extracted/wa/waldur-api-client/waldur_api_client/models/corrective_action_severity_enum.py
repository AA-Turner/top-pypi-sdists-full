from enum import Enum


class CorrectiveActionSeverityEnum(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"
    SAFE = "safe"

    def __str__(self) -> str:
        return str(self.value)
