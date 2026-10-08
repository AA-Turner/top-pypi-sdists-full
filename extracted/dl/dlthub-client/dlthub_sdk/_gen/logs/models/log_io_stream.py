from enum import Enum


class LogIoStream(str, Enum):
    OTHER = "other"
    STDERR = "stderr"
    STDOUT = "stdout"

    def __str__(self) -> str:
        return str(self.value)
