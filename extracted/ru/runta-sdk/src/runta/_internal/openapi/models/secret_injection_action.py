from enum import Enum


class SecretInjectionAction(str, Enum):
    HEADER = "header"
    QUERY = "query"

    def __str__(self) -> str:
        return str(self.value)
