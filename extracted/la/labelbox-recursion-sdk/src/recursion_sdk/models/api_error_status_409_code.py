from enum import StrEnum

class ApiErrorStatus409Code(StrEnum):
    CONFLICT = "conflict"

    def __str__(self) -> str:
        return str(self.value)
