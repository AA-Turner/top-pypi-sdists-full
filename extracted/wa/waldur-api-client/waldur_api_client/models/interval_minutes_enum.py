from enum import IntEnum


class IntervalMinutesEnum(IntEnum):
    VALUE_5 = 5
    VALUE_15 = 15
    VALUE_60 = 60

    def __str__(self) -> str:
        return str(self.value)
