from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class GetDataFrameRowDataFormat(Enums.KnownString):
    CSV = "csv"
    PARQUET = "parquet"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "GetDataFrameRowDataFormat":
        if not isinstance(val, str):
            raise ValueError(f"Value of GetDataFrameRowDataFormat must be a string (encountered: {val})")
        newcls = Enum("GetDataFrameRowDataFormat", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(GetDataFrameRowDataFormat, getattr(newcls, "_UNKNOWN"))
