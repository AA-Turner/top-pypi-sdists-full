from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyFragmentBinBinType(Enums.KnownString):
    FRAGMENT = "FRAGMENT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyFragmentBinBinType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblyFragmentBinBinType must be a string (encountered: {val})")
        newcls = Enum("AssemblyFragmentBinBinType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyFragmentBinBinType, getattr(newcls, "_UNKNOWN"))
