from enum import Enum


class HpcJobTimeWindowEnum(str, Enum):
    VALUE_0 = "1h"
    VALUE_1 = "8h"
    VALUE_2 = "24h"
    VALUE_3 = "3d"
    VALUE_4 = "7d"

    def __str__(self) -> str:
        return str(self.value)
