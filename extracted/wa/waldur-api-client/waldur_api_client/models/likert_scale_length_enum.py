from enum import IntEnum


class LikertScaleLengthEnum(IntEnum):
    VALUE_3 = 3
    VALUE_5 = 5
    VALUE_7 = 7

    def __str__(self) -> str:
        return str(self.value)
