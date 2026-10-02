from enum import StrEnum

class JobExecutionsResponseDtoExecutionsItemJobType(StrEnum):
    EXPORT = "export"
    IMPORT = "import"

    def __str__(self) -> str:
        return str(self.value)
