from enum import StrEnum

class ApiErrorStatus405Code(StrEnum):
    METHOD_NOT_ALLOWED = "method_not_allowed"

    def __str__(self) -> str:
        return str(self.value)
