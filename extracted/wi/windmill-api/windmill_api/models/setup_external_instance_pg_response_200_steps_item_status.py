from enum import Enum


class SetupExternalInstancePgResponse200StepsItemStatus(str, Enum):
    ERROR = "error"
    OK = "ok"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
