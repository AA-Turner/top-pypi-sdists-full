from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class DatasetsArchiveReason(Enums.KnownString):
    MADE_IN_ERROR = "Made in error"
    ARCHIVED = "Archived"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "DatasetsArchiveReason":
        if not isinstance(val, str):
            raise ValueError(f"Value of DatasetsArchiveReason must be a string (encountered: {val})")
        newcls = Enum("DatasetsArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(DatasetsArchiveReason, getattr(newcls, "_UNKNOWN"))
