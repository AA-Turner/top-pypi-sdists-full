from enum import Enum


class CascadeStepTypeEnum(str, Enum):
    SELECT_STRING = "select_string"
    SELECT_STRING_MULTI = "select_string_multi"

    def __str__(self) -> str:
        return str(self.value)
