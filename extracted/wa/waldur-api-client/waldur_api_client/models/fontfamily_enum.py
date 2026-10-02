from enum import Enum


class FONTFAMILYEnum(str, Enum):
    INTER = "Inter"
    MAVEN_PRO = "Maven Pro"

    def __str__(self) -> str:
        return str(self.value)
