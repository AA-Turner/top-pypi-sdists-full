from enum import StrEnum

class HealthOkResponseDtoStatus(StrEnum):
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
