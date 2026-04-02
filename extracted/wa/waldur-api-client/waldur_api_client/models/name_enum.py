from enum import Enum


class NameEnum(str, Enum):
    EESSI = "EESSI"
    SPACK = "Spack"

    def __str__(self) -> str:
        return str(self.value)
