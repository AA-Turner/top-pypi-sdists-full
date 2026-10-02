from enum import StrEnum

class ApiErrorStatus422Code(StrEnum):
    UNPROCESSABLE_ENTITY = "unprocessable_entity"

    def __str__(self) -> str:
        return str(self.value)
