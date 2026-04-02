from enum import Enum


class SystemLogOEnum(str, Enum):
    CREATED = "created"
    INSTANCE = "instance"
    LEVEL_NUMBER = "level_number"
    VALUE_0 = "-created"
    VALUE_1 = "-instance"
    VALUE_2 = "-level_number"

    def __str__(self) -> str:
        return str(self.value)
