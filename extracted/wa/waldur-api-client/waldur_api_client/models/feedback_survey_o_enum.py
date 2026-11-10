from enum import Enum


class FeedbackSurveyOEnum(str, Enum):
    ENDS_AT = "ends_at"
    NAME = "name"
    STARTS_AT = "starts_at"
    VALUE_0 = "-ends_at"
    VALUE_1 = "-name"
    VALUE_2 = "-starts_at"

    def __str__(self) -> str:
        return str(self.value)
