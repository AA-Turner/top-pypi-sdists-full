from enum import Enum


class ListFlowConversationsKind(str, Enum):
    ALL = "all"
    DEPLOYED = "deployed"
    TEST = "test"

    def __str__(self) -> str:
        return str(self.value)
