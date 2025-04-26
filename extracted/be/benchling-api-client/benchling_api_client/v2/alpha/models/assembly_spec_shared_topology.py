from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblySpecSharedTopology(Enums.KnownString):
    CIRCULAR = "CIRCULAR"
    LINEAR = "LINEAR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblySpecSharedTopology":
        if not isinstance(val, str):
            raise ValueError(f"Value of AssemblySpecSharedTopology must be a string (encountered: {val})")
        newcls = Enum("AssemblySpecSharedTopology", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblySpecSharedTopology, getattr(newcls, "_UNKNOWN"))
