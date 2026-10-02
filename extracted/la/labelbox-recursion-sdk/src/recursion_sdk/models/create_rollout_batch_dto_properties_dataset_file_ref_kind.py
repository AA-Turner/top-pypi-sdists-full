from enum import StrEnum

class CreateRolloutBatchDtoPropertiesDatasetFileRefKind(StrEnum):
    FILEREF = "fileRef"

    def __str__(self) -> str:
        return str(self.value)
