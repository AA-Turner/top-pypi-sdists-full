from enum import Enum


class JobType0FlowStatusFailureModuleAgentActionsItemType0Type(str, Enum):
    TOOL_CALL = "tool_call"

    def __str__(self) -> str:
        return str(self.value)
