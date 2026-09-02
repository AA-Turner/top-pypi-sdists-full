from enum import Enum


class ListTriggerHistoryResponse200ItemSource(str, Enum):
    API = "api"
    CLI = "cli"
    UI = "ui"
    WORKER = "worker"

    def __str__(self) -> str:
        return str(self.value)
