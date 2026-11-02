from enum import StrEnum

class DetailsCommentFormat(StrEnum):
    MARKDOWN = "markdown"

    def __str__(self) -> str:
        return str(self.value)
