from enum import StrEnum

class ManagedAgentsCreateAgentRequestToolsetsItemType(StrEnum):
    EVALUATION = "evaluation"

    def __str__(self) -> str:
        return str(self.value)
