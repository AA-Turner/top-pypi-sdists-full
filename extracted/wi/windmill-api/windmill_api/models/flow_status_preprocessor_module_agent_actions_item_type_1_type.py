from enum import Enum


class FlowStatusPreprocessorModuleAgentActionsItemType1Type(str, Enum):
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
