from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SelectorInputMultiValueUiBlockType(Enums.KnownString):
    SELECTOR_INPUT_MULTIVALUE = "SELECTOR_INPUT_MULTIVALUE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SelectorInputMultiValueUiBlockType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of SelectorInputMultiValueUiBlockType must be a string (encountered: {val})"
            )
        newcls = Enum("SelectorInputMultiValueUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SelectorInputMultiValueUiBlockType, getattr(newcls, "_UNKNOWN"))
