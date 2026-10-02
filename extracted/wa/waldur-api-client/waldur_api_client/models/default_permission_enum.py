from enum import Enum


class DefaultPermissionEnum(str, Enum):
    VALUE_0 = "2770"
    VALUE_1 = "2775"
    VALUE_2 = "2777"
    VALUE_3 = "770"
    VALUE_4 = "775"
    VALUE_5 = "777"

    def __str__(self) -> str:
        return str(self.value)
