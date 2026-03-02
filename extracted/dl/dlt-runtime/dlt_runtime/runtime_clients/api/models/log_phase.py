from enum import Enum


class LogPhase(str, Enum):
    PROGRAM = "program"
    SETUP = "setup"

    def __str__(self) -> str:
        return str(self.value)
