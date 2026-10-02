from enum import StrEnum

class ManagedAgentsAutomationDefinitionRunResponseStatus(StrEnum):
    CREATED = "created"
    FAILED = "failed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
