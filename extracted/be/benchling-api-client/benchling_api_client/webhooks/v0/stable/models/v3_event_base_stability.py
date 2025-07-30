from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class V3EventBaseStability(Enums.KnownString):
    STABLE = "stable"
    BETA = "beta"
    ALPHA = "alpha"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "V3EventBaseStability":
        if not isinstance(val, str):
            raise ValueError(f"Value of V3EventBaseStability must be a string (encountered: {val})")
        newcls = Enum("V3EventBaseStability", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(V3EventBaseStability, getattr(newcls, "_UNKNOWN"))
