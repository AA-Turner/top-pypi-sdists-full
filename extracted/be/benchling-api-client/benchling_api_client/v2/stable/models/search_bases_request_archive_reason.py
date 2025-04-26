from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SearchBasesRequestArchiveReason(Enums.KnownString):
    NOT_ARCHIVED = "NOT_ARCHIVED"
    OTHER = "Other"
    ARCHIVED = "Archived"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SearchBasesRequestArchiveReason":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of SearchBasesRequestArchiveReason must be a string (encountered: {val})"
            )
        newcls = Enum("SearchBasesRequestArchiveReason", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SearchBasesRequestArchiveReason, getattr(newcls, "_UNKNOWN"))
