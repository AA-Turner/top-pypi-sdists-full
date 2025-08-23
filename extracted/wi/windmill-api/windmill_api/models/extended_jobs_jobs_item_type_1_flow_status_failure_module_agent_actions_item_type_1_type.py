from enum import Enum


class ExtendedJobsJobsItemType1FlowStatusFailureModuleAgentActionsItemType1Type(str, Enum):
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
