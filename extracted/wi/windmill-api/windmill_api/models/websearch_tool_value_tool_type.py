from enum import Enum


class WebsearchToolValueToolType(str, Enum):
    WEBSEARCH = "websearch"

    def __str__(self) -> str:
        return str(self.value)
