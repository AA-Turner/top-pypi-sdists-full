from enum import Enum


class ProposalOEnum(str, Enum):
    CREATED = "created"
    ROUND_CALL_NAME = "round__call__name"
    ROUND_CUTOFF_TIME = "round__cutoff_time"
    ROUND_START_TIME = "round__start_time"
    SLUG = "slug"
    STATE = "state"
    VALUE_0 = "-created"
    VALUE_1 = "-round__call__name"
    VALUE_2 = "-round__cutoff_time"
    VALUE_3 = "-round__start_time"
    VALUE_4 = "-slug"
    VALUE_5 = "-state"

    def __str__(self) -> str:
        return str(self.value)
