from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class OptimizeCodonsMethod(Enums.KnownString):
    MATCH_CODON_USAGE = "MATCH_CODON_USAGE"
    USE_BEST_CODON = "USE_BEST_CODON"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "OptimizeCodonsMethod":
        if not isinstance(val, str):
            raise ValueError(f"Value of OptimizeCodonsMethod must be a string (encountered: {val})")
        newcls = Enum("OptimizeCodonsMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(OptimizeCodonsMethod, getattr(newcls, "_UNKNOWN"))
