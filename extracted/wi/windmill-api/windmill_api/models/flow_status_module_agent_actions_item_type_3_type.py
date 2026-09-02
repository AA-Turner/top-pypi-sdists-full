from enum import Enum


class FlowStatusModuleAgentActionsItemType3Type(str, Enum):
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
