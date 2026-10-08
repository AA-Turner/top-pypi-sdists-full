from enum import Enum


class RunSignalStage(str, Enum):
    BUILD = "build"
    RUN = "run"

    def __str__(self) -> str:
        return str(self.value)
