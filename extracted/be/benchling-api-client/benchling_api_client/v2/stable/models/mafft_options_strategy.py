from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MafftOptionsStrategy(Enums.KnownString):
    AUTO = "auto"
    SIXMER = "sixmer"
    LOCALPAIR = "localpair"
    GLOBALPAIR = "globalpair"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MafftOptionsStrategy":
        if not isinstance(val, str):
            raise ValueError(f"Value of MafftOptionsStrategy must be a string (encountered: {val})")
        newcls = Enum("MafftOptionsStrategy", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MafftOptionsStrategy, getattr(newcls, "_UNKNOWN"))
