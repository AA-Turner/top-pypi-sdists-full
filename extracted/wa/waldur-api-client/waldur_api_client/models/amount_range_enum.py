from enum import Enum


class AmountRangeEnum(str, Enum):
    NONE = "none"
    OVER_50K = "over_50k"
    UNDER_5K = "under_5k"
    VALUE_2 = "5k_10k"
    VALUE_3 = "10k_50k"

    def __str__(self) -> str:
        return str(self.value)
