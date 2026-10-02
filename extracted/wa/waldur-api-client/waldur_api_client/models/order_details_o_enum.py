from enum import Enum


class OrderDetailsOEnum(str, Enum):
    CONSUMER_REVIEWED_AT = "consumer_reviewed_at"
    COST = "cost"
    CREATED = "created"
    STATE = "state"
    VALUE_0 = "-consumer_reviewed_at"
    VALUE_1 = "-cost"
    VALUE_2 = "-created"
    VALUE_3 = "-state"

    def __str__(self) -> str:
        return str(self.value)
