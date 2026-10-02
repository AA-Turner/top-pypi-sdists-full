from enum import StrEnum

class ManagedAgentsAgentTemplateDefinitionToolsItemType(StrEnum):
    EVALUATION = "evaluation"

    def __str__(self) -> str:
        return str(self.value)
