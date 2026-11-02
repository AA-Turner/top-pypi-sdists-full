from enum import Enum


class ListJobsResponse200ItemType0FlowStatusModulesItemAgentActionsItemType0Type(str, Enum):
    TOOL_CALL = "tool_call"

    def __str__(self) -> str:
        return str(self.value)
