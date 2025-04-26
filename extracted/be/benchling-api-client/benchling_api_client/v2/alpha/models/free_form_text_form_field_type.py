from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FreeFormTextFormFieldType(Enums.KnownString):
    FREE_FORM_TEXT = "FREE_FORM_TEXT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FreeFormTextFormFieldType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FreeFormTextFormFieldType must be a string (encountered: {val})")
        newcls = Enum("FreeFormTextFormFieldType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FreeFormTextFormFieldType, getattr(newcls, "_UNKNOWN"))
