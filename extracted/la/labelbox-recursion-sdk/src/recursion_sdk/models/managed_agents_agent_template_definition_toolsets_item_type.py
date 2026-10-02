from enum import StrEnum

class ManagedAgentsAgentTemplateDefinitionToolsetsItemType(StrEnum):
    EVALUATION = "evaluation"

    def __str__(self) -> str:
        return str(self.value)
