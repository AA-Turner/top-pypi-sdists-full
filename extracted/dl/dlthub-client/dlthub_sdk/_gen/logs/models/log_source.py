from enum import Enum


class LogSource(str, Enum):
    RUNNER = "runner"
    SETUP = "setup"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
