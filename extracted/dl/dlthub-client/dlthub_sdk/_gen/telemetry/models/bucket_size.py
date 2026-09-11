from enum import Enum


class BucketSize(str, Enum):
    ALL = "all"
    VALUE_1 = "1h"
    VALUE_2 = "1d"
    VALUE_3 = "1w"
    VALUE_4 = "1m"
    VALUE_5 = "1y"

    def __str__(self) -> str:
        return str(self.value)
