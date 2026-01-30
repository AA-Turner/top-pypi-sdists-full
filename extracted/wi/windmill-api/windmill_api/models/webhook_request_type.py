from enum import Enum


class WebhookRequestType(str, Enum):
    ASYNC = "async"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
