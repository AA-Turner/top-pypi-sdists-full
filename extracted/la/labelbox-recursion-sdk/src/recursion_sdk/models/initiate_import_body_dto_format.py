from enum import StrEnum

class InitiateImportBodyDtoFormat(StrEnum):
    DEFAULT = "default"
    HARBOR_BASIC = "harbor-basic"

    def __str__(self) -> str:
        return str(self.value)
