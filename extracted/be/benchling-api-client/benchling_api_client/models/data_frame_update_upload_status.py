from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DataFrameUpdateUploadStatus(Enums.KnownString):
    IN_PROGRESS = "IN_PROGRESS"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DataFrameUpdateUploadStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of DataFrameUpdateUploadStatus must be a string (encountered: {val})")
        newcls = Enum("DataFrameUpdateUploadStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DataFrameUpdateUploadStatus, getattr(newcls, "_UNKNOWN"))
