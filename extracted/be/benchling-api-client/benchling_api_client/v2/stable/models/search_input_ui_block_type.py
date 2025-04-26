from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SearchInputUiBlockType(Enums.KnownString):
    SEARCH_INPUT = "SEARCH_INPUT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SearchInputUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of SearchInputUiBlockType must be a string (encountered: {val})")
        newcls = Enum("SearchInputUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SearchInputUiBlockType, getattr(newcls, "_UNKNOWN"))
