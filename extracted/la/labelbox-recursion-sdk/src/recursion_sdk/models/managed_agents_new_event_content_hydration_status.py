from enum import StrEnum

class ManagedAgentsNewEventContentHydrationStatus(StrEnum):
    CORRUPT = "corrupt"
    HYDRATED = "hydrated"
    MISSING = "missing"
    OVERSIZED = "oversized"
    REFS_ONLY = "refs_only"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
