from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FilesArchiveReason(Enums.KnownString):
    MADE_IN_ERROR = "Made in error"
    ARCHIVED = "Archived"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FilesArchiveReason":
        if not isinstance(val, str):
            raise ValueError(f"Value of FilesArchiveReason must be a string (encountered: {val})")
        newcls = Enum("FilesArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FilesArchiveReason, getattr(newcls, "_UNKNOWN"))
