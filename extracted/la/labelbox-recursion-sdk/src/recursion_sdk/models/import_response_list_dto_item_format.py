from enum import StrEnum

class ImportResponseListDtoItemFormat(StrEnum):
    HARBOR = "harbor"
    JSON = "json"
    TAR_GZ = "tar.gz"

    def __str__(self) -> str:
        return str(self.value)
