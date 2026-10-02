from enum import StrEnum

class ManagedAgentsMemoryStoreOrigin(StrEnum):
    CURATED = "curated"
    REFLECTION = "reflection"

    def __str__(self) -> str:
        return str(self.value)
