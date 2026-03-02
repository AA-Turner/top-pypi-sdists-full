from enum import Enum


class RunMode(str, Enum):
    ALWAYS = "always"
    WHEN_NOT_RUNNING = "when_not_running"

    def __str__(self) -> str:
        return str(self.value)
