from enum import Enum


class TriggerHistoryEntrySource(str, Enum):
    API = "api"
    CLI = "cli"
    UI = "ui"
    WORKER = "worker"

    def __str__(self) -> str:
        return str(self.value)
