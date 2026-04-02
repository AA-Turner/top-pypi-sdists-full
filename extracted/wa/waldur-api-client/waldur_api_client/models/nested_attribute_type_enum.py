from enum import Enum


class NestedAttributeTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    CHOICE = "choice"
    INTEGER = "integer"
    LIST = "list"
    STRING = "string"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
