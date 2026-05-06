from enum import Enum


class PresetEnum(str, Enum):
    CSCS = "cscs"
    OECD_FOS_2007 = "oecd_fos_2007"

    def __str__(self) -> str:
        return str(self.value)
