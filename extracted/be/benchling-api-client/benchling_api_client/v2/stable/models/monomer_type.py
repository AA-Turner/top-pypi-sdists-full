from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MonomerType(Enums.KnownString):
    BACKBONE = "BACKBONE"
    BRANCH = "BRANCH"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MonomerType":
        if not isinstance(val, str):
            raise ValueError(f"Value of MonomerType must be a string (encountered: {val})")
        newcls = Enum("MonomerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MonomerType, getattr(newcls, "_UNKNOWN"))
