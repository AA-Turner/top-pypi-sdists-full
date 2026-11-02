from enum import Enum


class CreateTemplateScriptJsonBodyLanguage(str, Enum):
    TYPESCRIPT = "Typescript"

    def __str__(self) -> str:
        return str(self.value)
