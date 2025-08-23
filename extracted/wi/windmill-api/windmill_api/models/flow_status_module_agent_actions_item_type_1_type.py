from enum import Enum


class FlowStatusModuleAgentActionsItemType1Type(str, Enum):
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
