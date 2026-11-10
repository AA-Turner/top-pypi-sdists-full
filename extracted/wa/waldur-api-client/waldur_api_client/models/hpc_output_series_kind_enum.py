from enum import Enum


class HpcOutputSeriesKindEnum(str, Enum):
    CSV = "csv"
    WRF_RSL = "wrf_rsl"
    XVG = "xvg"

    def __str__(self) -> str:
        return str(self.value)
