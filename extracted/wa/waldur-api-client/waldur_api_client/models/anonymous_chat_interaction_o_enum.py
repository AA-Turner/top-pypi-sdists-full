from enum import Enum


class AnonymousChatInteractionOEnum(str, Enum):
    CREATED = "created"
    RESULT_COUNT = "result_count"
    VALUE_0 = "-created"
    VALUE_1 = "-result_count"

    def __str__(self) -> str:
        return str(self.value)
