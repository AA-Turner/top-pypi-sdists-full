from enum import StrEnum

class ApiErrorStatus503Code(StrEnum):
    SERVICE_UNAVAILABLE = "service_unavailable"

    def __str__(self) -> str:
        return str(self.value)
