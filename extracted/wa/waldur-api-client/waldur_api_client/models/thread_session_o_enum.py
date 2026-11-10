from enum import Enum


class ThreadSessionOEnum(str, Enum):
    CACHE_RATIO = "cache_ratio"
    CACHE_READ_TOKENS = "cache_read_tokens"
    CACHE_WRITE_TOKENS = "cache_write_tokens"
    CREATED = "created"
    INPUT_TOKENS = "input_tokens"
    MODELS_USED = "models_used"
    MODIFIED = "modified"
    OUTPUT_TOKENS = "output_tokens"
    TOTAL_TOKENS = "total_tokens"
    VALUE_0 = "-cache_ratio"
    VALUE_1 = "-cache_read_tokens"
    VALUE_2 = "-cache_write_tokens"
    VALUE_3 = "-created"
    VALUE_4 = "-input_tokens"
    VALUE_5 = "-models_used"
    VALUE_6 = "-modified"
    VALUE_7 = "-output_tokens"
    VALUE_8 = "-total_tokens"

    def __str__(self) -> str:
        return str(self.value)
