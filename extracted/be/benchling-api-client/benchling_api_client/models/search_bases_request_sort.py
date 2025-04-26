from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SearchBasesRequestSort(Enums.KnownString):
    MODIFIEDATASC = "modifiedAt:asc"
    MODIFIEDATDESC = "modifiedAt:desc"
    NAMEASC = "name:asc"
    NAMEDESC = "name:desc"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SearchBasesRequestSort":
        if not isinstance(val, str):
            raise ValueError(f"Value of SearchBasesRequestSort must be a string (encountered: {val})")
        newcls = Enum("SearchBasesRequestSort", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SearchBasesRequestSort, getattr(newcls, "_UNKNOWN"))
