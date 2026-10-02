from enum import Enum


class LimitTypeEnum(str, Enum):
    GRPTRES = "GrpTRES"
    GRPTRESMINS = "GrpTRESMins"
    MAXTRESMINS = "MaxTRESMins"

    def __str__(self) -> str:
        return str(self.value)
