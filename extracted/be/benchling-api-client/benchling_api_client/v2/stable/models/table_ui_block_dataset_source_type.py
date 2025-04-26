from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class TableUiBlockDatasetSourceType(Enums.KnownString):
    DATASET = "DATASET"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "TableUiBlockDatasetSourceType":
        if not isinstance(val, str):
            raise ValueError(f"Value of TableUiBlockDatasetSourceType must be a string (encountered: {val})")
        newcls = Enum("TableUiBlockDatasetSourceType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(TableUiBlockDatasetSourceType, getattr(newcls, "_UNKNOWN"))
