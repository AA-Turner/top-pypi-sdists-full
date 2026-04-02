from enum import IntEnum


class GenderEnum(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_9 = 9

    def __str__(self) -> str:
        return str(self.value)
