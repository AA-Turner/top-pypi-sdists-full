from enum import Enum


class TJobDefinitionRefreshPropagation(str, Enum):
    ALWAYS = "always"
    AUTO = "auto"
    BLOCK = "block"

    def __str__(self) -> str:
        return str(self.value)
