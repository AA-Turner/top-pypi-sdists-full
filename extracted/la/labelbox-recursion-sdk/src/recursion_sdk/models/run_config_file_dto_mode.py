from enum import StrEnum

class RunConfigFileDtoMode(StrEnum):
    RO = "ro"
    RW = "rw"

    def __str__(self) -> str:
        return str(self.value)
