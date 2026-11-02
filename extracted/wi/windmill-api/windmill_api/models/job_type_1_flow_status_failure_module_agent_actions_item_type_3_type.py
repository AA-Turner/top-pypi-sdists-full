from enum import Enum


class JobType1FlowStatusFailureModuleAgentActionsItemType3Type(str, Enum):
    APPROVAL = "approval"

    def __str__(self) -> str:
        return str(self.value)
