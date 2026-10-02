from enum import StrEnum

class ListSessionEventsImageUrls(StrEnum):
    SIGNED = "signed"

    def __str__(self) -> str:
        return str(self.value)
