from enum import Enum


class AuthResultStateEnum(str, Enum):
    CANCELED = "Canceled"
    ERRED = "Erred"
    OK = "OK"
    PROCESSING = "Processing"
    SCHEDULED = "Scheduled"

    def __str__(self) -> str:
        return str(self.value)
