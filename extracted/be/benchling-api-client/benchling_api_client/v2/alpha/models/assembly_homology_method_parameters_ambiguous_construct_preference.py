from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyHomologyMethodParametersAmbiguousConstructPreference(Enums.KnownString):
    USE_LARGER_FRAGMENT_IN_FIRST_BIN = "USE_LARGER_FRAGMENT_IN_FIRST_BIN"
    USE_SMALER_FRAGMENT_IN_FIRST_BIN = "USE_SMALER_FRAGMENT_IN_FIRST_BIN"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyHomologyMethodParametersAmbiguousConstructPreference":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyHomologyMethodParametersAmbiguousConstructPreference must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyHomologyMethodParametersAmbiguousConstructPreference", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyHomologyMethodParametersAmbiguousConstructPreference, getattr(newcls, "_UNKNOWN"))
