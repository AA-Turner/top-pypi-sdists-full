from enum import Enum


class MatrixExportsDownloadRetrieveKind(str, Enum):
    EXPORT = "export"
    MEDIA = "media"

    def __str__(self) -> str:
        return str(self.value)
