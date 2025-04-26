from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AssemblyProteinReferencePolymerType(Enums.KnownString):
    AA_SEQUENCE = "AA_SEQUENCE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AssemblyProteinReferencePolymerType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AssemblyProteinReferencePolymerType must be a string (encountered: {val})"
            )
        newcls = Enum("AssemblyProteinReferencePolymerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AssemblyProteinReferencePolymerType, getattr(newcls, "_UNKNOWN"))
