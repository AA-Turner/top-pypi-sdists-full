from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FreeFormTextFormFieldDefaultKeyboard(Enums.KnownString):
    NUMERIC = "NUMERIC"
    DEFAULT = "DEFAULT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FreeFormTextFormFieldDefaultKeyboard":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of FreeFormTextFormFieldDefaultKeyboard must be a string (encountered: {val})"
            )
        newcls = Enum("FreeFormTextFormFieldDefaultKeyboard", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FreeFormTextFormFieldDefaultKeyboard, getattr(newcls, "_UNKNOWN"))
