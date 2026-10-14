from enum import Enum


class MatrixCryptoLeaseRequestKindEnum(str, Enum):
    BOOTSTRAP = "bootstrap"
    IMPORT = "import"
    RESET = "reset"

    def __str__(self) -> str:
        return str(self.value)
