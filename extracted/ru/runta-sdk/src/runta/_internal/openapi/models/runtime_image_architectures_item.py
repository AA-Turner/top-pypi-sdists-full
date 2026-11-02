from enum import Enum


class RuntimeImageArchitecturesItem(str, Enum):
    AARCH64 = "aarch64"
    X86_64 = "x86_64"

    def __str__(self) -> str:
        return str(self.value)
