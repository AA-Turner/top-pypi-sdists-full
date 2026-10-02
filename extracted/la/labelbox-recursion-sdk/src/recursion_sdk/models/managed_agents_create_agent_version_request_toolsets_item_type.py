from enum import StrEnum

class ManagedAgentsCreateAgentVersionRequestToolsetsItemType(StrEnum):
    EVALUATION = "evaluation"

    def __str__(self) -> str:
        return str(self.value)
