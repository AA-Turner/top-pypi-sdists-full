from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FormRawStringQueryValuePartType(Enums.KnownString):
    RAW_STRING = "RAW_STRING"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FormRawStringQueryValuePartType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of FormRawStringQueryValuePartType must be a string (encountered: {val})"
            )
        newcls = Enum("FormRawStringQueryValuePartType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FormRawStringQueryValuePartType, getattr(newcls, "_UNKNOWN"))
