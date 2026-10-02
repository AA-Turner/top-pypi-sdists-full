from enum import Enum


class ExportTypeEnum(str, Enum):
    MANUAL = "manual"
    ON_DELETION = "on_deletion"
    PERIODIC = "periodic"

    def __str__(self) -> str:
        return str(self.value)
