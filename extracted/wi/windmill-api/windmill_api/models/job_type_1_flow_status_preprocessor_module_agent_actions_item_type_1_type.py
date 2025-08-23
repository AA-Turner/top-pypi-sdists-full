from enum import Enum


class JobType1FlowStatusPreprocessorModuleAgentActionsItemType1Type(str, Enum):
    MESSAGE = "message"

    def __str__(self) -> str:
        return str(self.value)
