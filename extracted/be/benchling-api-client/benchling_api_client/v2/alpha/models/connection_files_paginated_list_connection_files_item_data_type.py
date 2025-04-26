from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ConnectionFilesPaginatedListConnectionFilesItemDataType(Enums.KnownString):
    ALLOTROPE = "ALLOTROPE"
    COMPENSATION = "COMPENSATION"
    DATACUBE = "DATACUBE"
    FRACTIONS = "FRACTIONS"
    GROUP = "GROUP"
    INJECTIONS = "INJECTIONS"
    MEASUREMENT = "MEASUREMENT"
    MEASUREMENT_SEPARATE_UNIT_COLUMN = "MEASUREMENT_SEPARATE_UNIT_COLUMN"
    ORIGINAL = "ORIGINAL"
    PEAKS = "PEAKS"
    PROCESSED = "PROCESSED"
    POPULATION = "POPULATION"
    REGION = "REGION"
    REPORT_POINT = "REPORT_POINT"
    REPORT = "REPORT"
    SAMPLE = "SAMPLE"
    SAMPLE_SEPARATE_UNIT_COLUMN = "SAMPLE_SEPARATE_UNIT_COLUMN"
    STATISTICS = "STATISTICS"
    TIMESERIES = "TIMESERIES"
    WELL = "WELL"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ConnectionFilesPaginatedListConnectionFilesItemDataType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of ConnectionFilesPaginatedListConnectionFilesItemDataType must be a string (encountered: {val})"
            )
        newcls = Enum("ConnectionFilesPaginatedListConnectionFilesItemDataType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ConnectionFilesPaginatedListConnectionFilesItemDataType, getattr(newcls, "_UNKNOWN"))
