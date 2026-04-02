from enum import Enum


class ImpactLevelDisplayEnum(str, Enum):
    DEGRADED_PERFORMANCE = "Degraded performance"
    FULL_OUTAGE = "Full outage"
    NO_IMPACT = "No impact"
    PARTIAL_OUTAGE = "Partial outage"

    def __str__(self) -> str:
        return str(self.value)
