from enum import Enum


class FlowStatusFailureModuleAgentActionsItemType3Type(str, Enum):
    APPROVAL = "approval"

    def __str__(self) -> str:
        return str(self.value)
