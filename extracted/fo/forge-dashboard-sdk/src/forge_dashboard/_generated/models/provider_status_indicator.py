from enum import StrEnum

class ProviderStatusIndicator(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
