from enum import Enum


class ExecutionModeEnum(str, Enum):
    EMULATOR = "emulator"
    PRODUCTION = "production"

    def __str__(self) -> str:
        return str(self.value)
