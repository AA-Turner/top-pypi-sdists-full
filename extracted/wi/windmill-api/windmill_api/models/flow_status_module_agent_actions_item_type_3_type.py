from enum import Enum


class FlowStatusModuleAgentActionsItemType3Type(str, Enum):
    APPROVAL = "approval"

    def __str__(self) -> str:
        return str(self.value)
