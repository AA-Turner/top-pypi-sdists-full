from enum import StrEnum

class ManagedAgentsCreateAgentRequestToolsItemType(StrEnum):
    EVALUATION = "evaluation"

    def __str__(self) -> str:
        return str(self.value)
