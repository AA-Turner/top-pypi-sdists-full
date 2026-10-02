from enum import StrEnum

class GetSessionTreeImageUrls(StrEnum):
    SIGNED = "signed"

    def __str__(self) -> str:
        return str(self.value)
