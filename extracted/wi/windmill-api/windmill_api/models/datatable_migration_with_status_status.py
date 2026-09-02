from enum import Enum


class DatatableMigrationWithStatusStatus(str, Enum):
    NOT_RUN = "not_run"
    RAN = "ran"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
