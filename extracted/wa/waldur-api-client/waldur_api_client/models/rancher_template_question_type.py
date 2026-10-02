from enum import Enum


class RancherTemplateQuestionType(str, Enum):
    BOOLEAN = "boolean"
    ENUM = "enum"
    SECRET = "secret"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
