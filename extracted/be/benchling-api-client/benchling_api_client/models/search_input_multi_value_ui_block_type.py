from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SearchInputMultiValueUiBlockType(Enums.KnownString):
    SEARCH_INPUT_MULTIVALUE = "SEARCH_INPUT_MULTIVALUE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SearchInputMultiValueUiBlockType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of SearchInputMultiValueUiBlockType must be a string (encountered: {val})"
            )
        newcls = Enum("SearchInputMultiValueUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SearchInputMultiValueUiBlockType, getattr(newcls, "_UNKNOWN"))
