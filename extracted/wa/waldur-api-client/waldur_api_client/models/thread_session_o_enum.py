from enum import Enum


class ThreadSessionOEnum(str, Enum):
    CREATED = "created"
    INPUT_TOKENS = "input_tokens"
    MODELS_USED = "models_used"
    MODIFIED = "modified"
    OUTPUT_TOKENS = "output_tokens"
    TOTAL_TOKENS = "total_tokens"
    VALUE_0 = "-created"
    VALUE_1 = "-input_tokens"
    VALUE_2 = "-models_used"
    VALUE_3 = "-modified"
    VALUE_4 = "-output_tokens"
    VALUE_5 = "-total_tokens"

    def __str__(self) -> str:
        return str(self.value)
