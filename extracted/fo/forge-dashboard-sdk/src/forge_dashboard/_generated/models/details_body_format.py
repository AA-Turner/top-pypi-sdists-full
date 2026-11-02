from enum import StrEnum

class DetailsBodyFormat(StrEnum):
    MARKDOWN = "markdown"

    def __str__(self) -> str:
        return str(self.value)
