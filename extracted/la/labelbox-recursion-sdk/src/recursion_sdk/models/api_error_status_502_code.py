from enum import StrEnum

class ApiErrorStatus502Code(StrEnum):
    BAD_GATEWAY = "bad_gateway"

    def __str__(self) -> str:
        return str(self.value)
