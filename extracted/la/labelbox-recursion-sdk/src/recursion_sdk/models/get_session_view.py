from enum import StrEnum

class GetSessionView(StrEnum):
    FULL = "full"
    SUMMARY = "summary"

    def __str__(self) -> str:
        return str(self.value)
