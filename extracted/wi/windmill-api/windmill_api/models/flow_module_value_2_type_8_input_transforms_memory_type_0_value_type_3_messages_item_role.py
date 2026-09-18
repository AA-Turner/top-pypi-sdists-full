from enum import Enum


class FlowModuleValue2Type8InputTransformsMemoryType0ValueType3MessagesItemRole(str, Enum):
    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
