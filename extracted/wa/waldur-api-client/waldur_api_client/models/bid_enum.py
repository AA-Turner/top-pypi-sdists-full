from enum import Enum


class BidEnum(str, Enum):
    CONFLICT = "conflict"
    EAGER = "eager"
    NOT_WILLING = "not_willing"
    WILLING = "willing"

    def __str__(self) -> str:
        return str(self.value)
