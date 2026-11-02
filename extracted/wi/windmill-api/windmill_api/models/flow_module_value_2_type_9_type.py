from enum import Enum


class FlowModuleValue2Type9Type(str, Enum):
    AIDECISION = "aidecision"

    def __str__(self) -> str:
        return str(self.value)
