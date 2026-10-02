from enum import Enum


class BackendResourceReqStateEnum(str, Enum):
    DONE = "Done"
    ERRED = "Erred"
    PROCESSING = "Processing"
    SENT = "Sent"

    def __str__(self) -> str:
        return str(self.value)
