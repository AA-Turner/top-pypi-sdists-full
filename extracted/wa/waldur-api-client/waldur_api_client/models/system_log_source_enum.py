from enum import Enum


class SystemLogSourceEnum(str, Enum):
    API = "api"
    BEAT = "beat"
    WORKER = "worker"

    def __str__(self) -> str:
        return str(self.value)
