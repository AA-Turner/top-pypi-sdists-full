from enum import StrEnum

class ProblemRunFileWithDownloadUrlListDtoItemType(StrEnum):
    OUTPUT = "output"

    def __str__(self) -> str:
        return str(self.value)
