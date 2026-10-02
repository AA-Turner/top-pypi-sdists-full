from enum import Enum


class MatrixHistoryExportStateEnum(str, Enum):
    COMPLETED = "completed"
    EXPORTING = "exporting"
    FAILED = "failed"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
