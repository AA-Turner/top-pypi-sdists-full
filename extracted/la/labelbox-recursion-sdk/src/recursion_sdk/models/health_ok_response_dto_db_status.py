from enum import StrEnum

class HealthOkResponseDtoDbStatus(StrEnum):
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
