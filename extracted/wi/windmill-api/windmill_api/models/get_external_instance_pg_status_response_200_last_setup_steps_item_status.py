from enum import Enum


class GetExternalInstancePgStatusResponse200LastSetupStepsItemStatus(str, Enum):
    ERROR = "error"
    OK = "ok"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
