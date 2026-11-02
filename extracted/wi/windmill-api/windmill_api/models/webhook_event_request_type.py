from enum import Enum


class WebhookEventRequestType(str, Enum):
    ASYNC = "async"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
