from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class SecureTextAppConfigItemType(Enums.KnownString):
    SECURE_TEXT = "secure_text"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "SecureTextAppConfigItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of SecureTextAppConfigItemType must be a string (encountered: {val})")
        newcls = Enum("SecureTextAppConfigItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(SecureTextAppConfigItemType, getattr(newcls, "_UNKNOWN"))
