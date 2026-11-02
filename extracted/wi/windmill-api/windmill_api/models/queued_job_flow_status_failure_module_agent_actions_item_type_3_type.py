from enum import Enum


class QueuedJobFlowStatusFailureModuleAgentActionsItemType3Type(str, Enum):
    APPROVAL = "approval"

    def __str__(self) -> str:
        return str(self.value)
