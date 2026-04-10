from enum import Enum


class ThreadSessionOEnum(str, Enum):
    CREATED = "created"
    INPUT_TOKENS = "input_tokens"
    MODIFIED = "modified"
    OUTPUT_TOKENS = "output_tokens"
    TOTAL_TOKENS = "total_tokens"
    VALUE_0 = "-created"
    VALUE_1 = "-input_tokens"
    VALUE_2 = "-modified"
    VALUE_3 = "-output_tokens"
    VALUE_4 = "-total_tokens"

    def __str__(self) -> str:
        return str(self.value)
