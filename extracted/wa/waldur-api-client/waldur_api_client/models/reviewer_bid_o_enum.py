from enum import Enum


class ReviewerBidOEnum(str, Enum):
    BID = "bid"
    MODIFIED_AT = "modified_at"
    SUBMITTED_AT = "submitted_at"
    VALUE_0 = "-bid"
    VALUE_1 = "-modified_at"
    VALUE_2 = "-submitted_at"

    def __str__(self) -> str:
        return str(self.value)
