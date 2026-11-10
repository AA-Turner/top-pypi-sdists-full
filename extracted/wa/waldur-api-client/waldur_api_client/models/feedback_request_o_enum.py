from enum import Enum


class FeedbackRequestOEnum(str, Enum):
    ANSWERED_AT = "answered_at"
    CREATED = "created"
    PROMPT_COUNT = "prompt_count"
    STATE = "state"
    VALUE_0 = "-answered_at"
    VALUE_1 = "-created"
    VALUE_2 = "-prompt_count"
    VALUE_3 = "-state"

    def __str__(self) -> str:
        return str(self.value)
