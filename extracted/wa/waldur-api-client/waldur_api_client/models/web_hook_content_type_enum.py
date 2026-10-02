from enum import Enum


class WebHookContentTypeEnum(str, Enum):
    FORM = "form"
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)
