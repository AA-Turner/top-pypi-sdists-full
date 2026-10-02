from enum import StrEnum

class ManagedAgentsOutcomeRubricRefType(StrEnum):
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
