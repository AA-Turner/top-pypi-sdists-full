from enum import Enum


class TemplateScriptLanguage(str, Enum):
    TYPESCRIPT = "Typescript"

    def __str__(self) -> str:
        return str(self.value)
