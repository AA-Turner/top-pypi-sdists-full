from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TableUiBlockDataFrameSourceType(Enums.KnownString):
    DATA_FRAME = "DATA_FRAME"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TableUiBlockDataFrameSourceType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of TableUiBlockDataFrameSourceType must be a string (encountered: {val})"
            )
        newcls = Enum("TableUiBlockDataFrameSourceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TableUiBlockDataFrameSourceType, getattr(newcls, "_UNKNOWN"))
