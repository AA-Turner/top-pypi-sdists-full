from enum import Enum


class CreateRuntimeImageBuildRequestArchitecture(str, Enum):
    X86_64 = "x86_64"

    def __str__(self) -> str:
        return str(self.value)
